// qkernel: exact statevector simulation of the Z / ZZ feature maps and the fidelity kernel.
//
// Build:  cmake -S cpp -B cpp/build -DCMAKE_BUILD_TYPE=Release && cmake --build cpp/build
// Usage:  qkernel <z|zz> <reps> <angles_train.bin> <angles_other.bin> <out_kernel.bin>
//   input  .bin: int64 rows, int64 cols, then rows*cols float64 (row-major)
//   output .bin: int64 rows_other, int64 rows_train, then the kernel matrix (float64)
//
// Each repetition is: H on every qubit (in-place Walsh-Hadamard transform), then a diagonal
// phase exp(i*phase(b)) with phase(b) = sum_i 2 x_i b_i + sum_(i,i+1) 2 (pi-x_i)(pi-x_j) (b_i XOR b_j).
// Qubit i is bit i of the basis index, matching the Python engine and Qiskit.
#include <chrono>
#include <cmath>
#include <complex>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using cd = std::complex<double>;

struct Matrix {
  int64_t rows = 0, cols = 0;
  std::vector<double> v;
};

static Matrix read_bin(const std::string& path) {
  std::ifstream f(path, std::ios::binary);
  if (!f) throw std::runtime_error("cannot open " + path);
  Matrix m;
  f.read(reinterpret_cast<char*>(&m.rows), 8);
  f.read(reinterpret_cast<char*>(&m.cols), 8);
  m.v.resize(m.rows * m.cols);
  f.read(reinterpret_cast<char*>(m.v.data()), 8 * m.v.size());
  return m;
}

static void walsh_hadamard(std::vector<cd>& psi) {
  const size_t dim = psi.size();
  for (size_t h = 1; h < dim; h <<= 1)
    for (size_t i = 0; i < dim; i += 2 * h)
      for (size_t j = i; j < i + h; ++j) {
        cd a = psi[j], b = psi[j + h];
        psi[j] = a + b;
        psi[j + h] = a - b;
      }
  const double norm = 1.0 / std::sqrt(static_cast<double>(dim));
  for (auto& z : psi) z *= norm;
}

static std::vector<cd> state(const double* x, int n, bool zz, int reps) {
  const size_t dim = size_t(1) << n;
  std::vector<double> phase(dim, 0.0);
  for (size_t b = 0; b < dim; ++b) {
    double p = 0.0;
    for (int i = 0; i < n; ++i)
      if ((b >> i) & 1) p += 2.0 * x[i];
    if (zz)
      for (int i = 0; i + 1 < n; ++i)
        if ((((b >> i) ^ (b >> (i + 1))) & 1)) p += 2.0 * (M_PI - x[i]) * (M_PI - x[i + 1]);
    phase[b] = p;
  }
  std::vector<cd> D(dim), psi(dim);
  for (size_t b = 0; b < dim; ++b) D[b] = std::polar(1.0, phase[b]);
  const double amp = 1.0 / std::sqrt(static_cast<double>(dim));
  for (size_t b = 0; b < dim; ++b) psi[b] = amp * D[b];  // first H^n acting on |0...0>
  for (int r = 1; r < reps; ++r) {
    walsh_hadamard(psi);
    for (size_t b = 0; b < dim; ++b) psi[b] *= D[b];
  }
  return psi;
}

int main(int argc, char** argv) {
  if (argc != 6) {
    std::cerr << "usage: qkernel <z|zz> <reps> <train.bin> <other.bin> <out.bin>\n";
    return 1;
  }
  const bool zz = std::string(argv[1]) == "zz";
  const int reps = std::stoi(argv[2]);
  Matrix A = read_bin(argv[3]), B = read_bin(argv[4]);
  if (A.cols != B.cols) throw std::runtime_error("column mismatch");
  const int n = static_cast<int>(A.cols);

  auto t0 = std::chrono::steady_clock::now();
  std::vector<std::vector<cd>> SA(A.rows), SB(B.rows);
#pragma omp parallel for schedule(static)
  for (int64_t i = 0; i < A.rows; ++i) SA[i] = state(&A.v[i * n], n, zz, reps);
#pragma omp parallel for schedule(static)
  for (int64_t i = 0; i < B.rows; ++i) SB[i] = state(&B.v[i * n], n, zz, reps);

  std::vector<double> K(B.rows * A.rows);
  const size_t dim = size_t(1) << n;
#pragma omp parallel for schedule(dynamic)
  for (int64_t i = 0; i < B.rows; ++i)
    for (int64_t j = 0; j < A.rows; ++j) {
      cd s = 0.0;
      const cd* a = SB[i].data();
      const cd* b = SA[j].data();
      for (size_t k = 0; k < dim; ++k) s += std::conj(a[k]) * b[k];
      K[i * A.rows + j] = std::norm(s);
    }
  double secs = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();

  std::ofstream f(argv[5], std::ios::binary);
  f.write(reinterpret_cast<const char*>(&B.rows), 8);
  f.write(reinterpret_cast<const char*>(&A.rows), 8);
  f.write(reinterpret_cast<const char*>(K.data()), 8 * K.size());
  std::printf("%.6f\n", secs);
  return 0;
}
