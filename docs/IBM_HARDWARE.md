# Running on IBM Quantum hardware

The main study runs on an exact statevector simulator. This is a small check that the
kernels survive real hardware noise, using IBM's free Open Plan (10 QPU minutes per 28 days).

## 1. One-time setup (on your own computer)

```powershell
pip install qiskit qiskit-ibm-runtime qiskit-aer
```

Get your API key from https://quantum.cloud.ibm.com (create one under "API key") and, if
shown, your instance CRN. Save them **once**, typing them only into your own terminal:

```powershell
python -c "from qiskit_ibm_runtime import QiskitRuntimeService as S; S.save_account(channel='ibm_quantum_platform', token=input('API key: '), instance=input('Instance CRN (Enter to skip): ') or None, overwrite=True)"
```

This stores the key in `~/.qiskit/qiskit-ibm.json`, outside the repository. Never paste the
key into code, configs, notebooks, chats or commits. If it ever leaks, delete it on the IBM
dashboard and create a new one.

Check it works:

```powershell
python -c "from qiskit_ibm_runtime import QiskitRuntimeService as S; print([b.name for b in S().backends()])"
```

## 2. Rehearse on a fake device (free, unlimited)

```powershell
python scripts/ibm_hardware_run.py --mode fake
```

This uses a noise model of a real IBM processor. Check the output makes sense first.

## 3. Real hardware

```powershell
python scripts/ibm_hardware_run.py --mode real
```

It prints the circuit count and a rough QPU-time estimate and asks before submitting.
Jobs wait in a queue, possibly for hours; job ids are saved to `results/hardware/pending_jobs.json`.
If you close the terminal, collect results later with:

```powershell
python scripts/ibm_hardware_run.py --mode real --retrieve <job_id> <job_id> ...
```

To spend fewer minutes, run only the projected kernel (3 circuits per event instead of one
per pair): add `--no-fidelity`.

## What to report

Hardware vs exact AUC and kernel error on the same events, the device name, date and job ids.
With ~24 test events the AUC is a demonstration that the pipeline runs on hardware, not a
headline result.
