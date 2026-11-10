// qkernel: exact statevector simulation of the Z / ZZ feature maps and the fidelity kernel.
//
// Build:  cmake -S cpp -B cpp/build -DCMAKE_BUILD_TYPE=Release && cmake --build cpp/build --config Release
//         (works with GCC, Clang and MSVC; on MSVC the binary is cpp/build/Release/qkernel.exe)
//         Windows/MinGW (WinLibs GCC): install it in a path without spaces (e.g. C:\tools\winlibs),
//         since MinGW's linker cannot find default-manifest.o under a path with spaces, then
//         cmake -S cpp -B cpp/build -G Ninja -DCMAKE_BUILD_TYPE=Release && cmake --build cpp/build
// Usage:  qkernel <z|zz> <reps> <angles_train.bin> <angles_other.bin> <out_kernel.bin>
//   input  .bin: int64 rows, int64 cols, then rows*cols float64 (row-major)
//   output .bin: int64 rows_other, int64 rows_train, then the kernel matrix (float64)
//   stdout: "total states kernel" seconds (total = states + kernel; file I/O excluded)
//
// Each repetition is: H on every qubit (in-place Walsh-Hadamard transform), then a diagonal
// phase exp(i*phase(b)) with phase(b) = sum_i 2 x_i b_i + sum_(i,i+1) 2 (pi-x_i)(pi-x_j) (b_i XOR b_j).
// Qubit i is bit i of the basis index, matching the Python engine and Qiskit.
//
// Layout and performance:
//  - States are stored structure-of-arrays: one contiguous, 64-byte aligned block of real parts
//    and one of imaginary parts, row s at offset s*dim. The Walsh-Hadamard transform and the
//    phase multiply are then plain real loops that vectorise.
//  - K[i][j] = |<b_i|a_j>|^2 with <b|a> = sum_k (br ar + bi ai) + i (br ai - bi ar). The kernel
//    is computed in tiles of TILE x TILE states; within a tile the amplitude index k is split
//    into chunks of KC so the tile's working set stays in L2, and a 2x2 register-blocked
//    micro-kernel (8 accumulators, omp simd reduction) computes four inner products per pass,
//    so every loaded amplitude is used twice. Tiles are distributed over OpenMP threads.
//  - Symmetry of K(X, X) is deliberately NOT exploited, to stay comparable with NumPy's GEMM.
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <new>
#include <stdexcept>
#include <string>
#include <vector>

constexpr double kPi = 3.14159265358979323846;  // portable pi (the POSIX macro is missing on MSVC)
constexpr int64_t TILE = 32;    // states per tile side
constexpr size_t KC = 512;      // amplitudes per k-chunk: 2 x (2*TILE) x KC x 8 B = 512 KiB
constexpr size_t ALIGN = 64;

#if defined(_MSC_VER)
#define RESTRICT __restrict
#else
#define RESTRICT __restrict__
#endif

struct Matrix {
  int64_t rows = 0, cols = 0;
  std::vector<double> v;
};

// 64-byte aligned array of doubles (std::vector cannot guarantee the alignment pre-C++17 allocators).
struct AlignedBuf {
  double* p = nullptr;
  explicit AlignedBuf(size_t n) {
    p = static_cast<double*>(::operator new[](n * sizeof(double), std::align_val_t(ALIGN)));
  }
  ~AlignedBuf() { ::operator delete[](p, std::align_val_t(ALIGN)); }
  AlignedBuf(const AlignedBuf&) = delete;
  AlignedBuf& operator=(const AlignedBuf&) = delete;
};

// Structure-of-arrays batch of statevectors.
struct States {
  int64_t count;
  size_t dim;
  AlignedBuf re, im;
  States(int64_t c, size_t d) : count(c), dim(d), re(size_t(c) * d), im(size_t(c) * d) {}
  double* r(int64_t s) { return re.p + size_t(s) * dim; }
  double* i(int64_t s) { return im.p + size_t(s) * dim; }
  const double* r(int64_t s) const { return re.p + size_t(s) * dim; }
  const double* i(int64_t s) const { return im.p + size_t(s) * dim; }
};

static Matrix read_bin(const std::string& path) {
  std::ifstream f(path, std::ios::binary);
  if (!f) throw std::runtime_error("cannot open " + path);
  Matrix m;
  f.read(reinterpret_cast<char*>(&m.rows), 8);
  f.read(reinterpret_cast<char*>(&m.cols), 8);
  if (!f || m.rows < 0 || m.cols <= 0 || m.cols > 30) throw std::runtime_error("bad header in " + path);
  m.v.resize(size_t(m.rows * m.cols));
  f.read(reinterpret_cast<char*>(m.v.data()), std::streamsize(8 * m.v.size()));
  if (!f) throw std::runtime_error("truncated " + path);
  return m;
}

// Unnormalised in-place Walsh-Hadamard transform of one real array.
static void wht(double* RESTRICT v, size_t dim) {
  for (size_t h = 1; h < dim; h <<= 1)
    for (size_t i = 0; i < dim; i += 2 * h) {
      double* RESTRICT lo = v + i;
      double* RESTRICT hi = v + i + h;
#pragma omp simd
      for (size_t j = 0; j < h; ++j) {
        const double a = lo[j], b = hi[j];
        lo[j] = a + b;
        hi[j] = a - b;
      }
    }
}

// Fills (re, im) with U(x)|0...0>. dr, di are scratch arrays of length dim for the diagonal.
static void build_state(const double* x, int n, bool zz, int reps, double* RESTRICT re, double* RESTRICT im,
                        double* RESTRICT dr, double* RESTRICT di) {
  const size_t dim = size_t(1) << n;
  for (size_t b = 0; b < dim; ++b) {
    double p = 0.0;
    for (int q = 0; q < n; ++q)
      if ((b >> q) & 1) p += 2.0 * x[q];
    if (zz)
      for (int q = 0; q + 1 < n; ++q)
        if ((((b >> q) ^ (b >> (q + 1))) & 1)) p += 2.0 * (kPi - x[q]) * (kPi - x[q + 1]);
    dr[b] = std::cos(p);
    di[b] = std::sin(p);
  }
  const double amp = 1.0 / std::sqrt(static_cast<double>(dim));
#pragma omp simd
  for (size_t b = 0; b < dim; ++b) {  // first H^n acting on |0...0>, then D
    re[b] = amp * dr[b];
    im[b] = amp * di[b];
  }
  for (int r = 1; r < reps; ++r) {
    wht(re, dim);
    wht(im, dim);
#pragma omp simd
    for (size_t b = 0; b < dim; ++b) {  // (re + i im) * (dr + i di) / sqrt(dim)
      const double a = re[b] * amp, c = im[b] * amp;
      re[b] = a * dr[b] - c * di[b];
      im[b] = a * di[b] + c * dr[b];
    }
  }
}

static void build_all(const Matrix& X, bool zz, int reps, States& S) {
  const int n = static_cast<int>(X.cols);
#pragma omp parallel
  {
    std::vector<double> dr(S.dim), di(S.dim);
#pragma omp for schedule(static)
    for (int64_t s = 0; s < X.rows; ++s)
      build_state(&X.v[size_t(s * n)], n, zz, reps, S.r(s), S.i(s), dr.data(), di.data());
  }
}

// K[i * NA + j] = |<B_i | A_j>|^2.
static void fidelity(const States& A, const States& B, std::vector<double>& K) {
  const int64_t NA = A.count, NB = B.count;
  const size_t dim = A.dim;
  const int64_t ti = (NB + TILE - 1) / TILE, tj = (NA + TILE - 1) / TILE;
#pragma omp parallel
  {
    std::vector<double> accr(TILE * TILE), acci(TILE * TILE);
#pragma omp for schedule(dynamic) collapse(2)
    for (int64_t bi = 0; bi < ti; ++bi)
      for (int64_t bj = 0; bj < tj; ++bj) {
        const int64_t i0 = bi * TILE, i1 = std::min(NB, i0 + TILE);
        const int64_t j0 = bj * TILE, j1 = std::min(NA, j0 + TILE);
        std::fill(accr.begin(), accr.end(), 0.0);
        std::fill(acci.begin(), acci.end(), 0.0);
        for (size_t k0 = 0; k0 < dim; k0 += KC) {
          const size_t len = std::min(KC, dim - k0);
          for (int64_t i = i0; i < i1; i += 2) {
            const bool two_i = i + 1 < i1;
            const double* RESTRICT b0r = B.r(i) + k0;
            const double* RESTRICT b0i = B.i(i) + k0;
            const double* RESTRICT b1r = B.r(two_i ? i + 1 : i) + k0;
            const double* RESTRICT b1i = B.i(two_i ? i + 1 : i) + k0;
            for (int64_t j = j0; j < j1; j += 2) {
              const bool two_j = j + 1 < j1;
              const double* RESTRICT a0r = A.r(j) + k0;
              const double* RESTRICT a0i = A.i(j) + k0;
              const double* RESTRICT a1r = A.r(two_j ? j + 1 : j) + k0;
              const double* RESTRICT a1i = A.i(two_j ? j + 1 : j) + k0;
              double r00 = 0, i00 = 0, r01 = 0, i01 = 0, r10 = 0, i10 = 0, r11 = 0, i11 = 0;
#pragma omp simd reduction(+ : r00, i00, r01, i01, r10, i10, r11, i11)
              for (size_t k = 0; k < len; ++k) {
                const double xr0 = b0r[k], xi0 = b0i[k], xr1 = b1r[k], xi1 = b1i[k];
                const double yr0 = a0r[k], yi0 = a0i[k], yr1 = a1r[k], yi1 = a1i[k];
                r00 += xr0 * yr0 + xi0 * yi0;  i00 += xr0 * yi0 - xi0 * yr0;
                r01 += xr0 * yr1 + xi0 * yi1;  i01 += xr0 * yi1 - xi0 * yr1;
                r10 += xr1 * yr0 + xi1 * yi0;  i10 += xr1 * yi0 - xi1 * yr0;
                r11 += xr1 * yr1 + xi1 * yi1;  i11 += xr1 * yi1 - xi1 * yr1;
              }
              const int64_t li = i - i0, lj = j - j0;
              accr[li * TILE + lj] += r00;  acci[li * TILE + lj] += i00;
              if (two_j) { accr[li * TILE + lj + 1] += r01;  acci[li * TILE + lj + 1] += i01; }
              if (two_i) { accr[(li + 1) * TILE + lj] += r10;  acci[(li + 1) * TILE + lj] += i10; }
              if (two_i && two_j) { accr[(li + 1) * TILE + lj + 1] += r11;  acci[(li + 1) * TILE + lj + 1] += i11; }
            }
          }
        }
        for (int64_t i = i0; i < i1; ++i)
          for (int64_t j = j0; j < j1; ++j) {
            const double re = accr[(i - i0) * TILE + (j - j0)], im = acci[(i - i0) * TILE + (j - j0)];
            K[size_t(i * NA + j)] = re * re + im * im;
          }
      }
  }
}

int main(int argc, char** argv) {
  try {
    if (argc != 6) {
      std::cerr << "usage: qkernel <z|zz> <reps> <train.bin> <other.bin> <out.bin>\n";
      return 1;
    }
    const std::string kind = argv[1];
    if (kind != "z" && kind != "zz") throw std::runtime_error("feature map must be z or zz");
    const bool zz = kind == "zz";
    const int reps = std::stoi(argv[2]);
    if (reps < 1) throw std::runtime_error("reps must be >= 1");
    Matrix A = read_bin(argv[3]), B = read_bin(argv[4]);
    if (A.cols != B.cols) throw std::runtime_error("column mismatch");
    const size_t dim = size_t(1) << A.cols;

    using clock = std::chrono::steady_clock;
    const auto t0 = clock::now();
    States SA(A.rows, dim), SB(B.rows, dim);
    build_all(A, zz, reps, SA);
    build_all(B, zz, reps, SB);
    const auto t1 = clock::now();
    std::vector<double> K(size_t(B.rows * A.rows));
    fidelity(SA, SB, K);
    const auto t2 = clock::now();
    const double secs = std::chrono::duration<double>(t2 - t0).count();
    const double states_s = std::chrono::duration<double>(t1 - t0).count();
    const double kernel_s = std::chrono::duration<double>(t2 - t1).count();

    std::ofstream f(argv[5], std::ios::binary);
    f.write(reinterpret_cast<const char*>(&B.rows), 8);
    f.write(reinterpret_cast<const char*>(&A.rows), 8);
    f.write(reinterpret_cast<const char*>(K.data()), std::streamsize(8 * K.size()));
    if (!f) throw std::runtime_error("cannot write output");
    std::printf("%.6f %.6f %.6f\n", secs, states_s, kernel_s);
    return 0;
  } catch (const std::exception& e) {
    std::cerr << "qkernel: " << e.what() << "\n";
    return 2;
  }
}
