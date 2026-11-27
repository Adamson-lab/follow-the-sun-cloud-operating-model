.PHONY: demo test verify lint clean

demo:
	python3 src/solar_shift_router/dispatcher.py --utc-hour 2 --utc-minute 30 --enclave commercial-global
	python3 src/solar_shift_router/dispatcher.py --utc-hour 2 --utc-minute 30 --enclave fedramp-high-us
	python3 src/handover_state_compiler/compiler.py --outgoing-pod AMER --incoming-pod APAC --utc-hour 20 --utc-minute 30

test:
	python3 -m unittest discover -s tests -p "test_*.py" -v

verify:
	python3 src/merkle_handover_ledger/verifier.py --ledger evidence/merkle-receipts/latest_handover_proof.json

lint:
	python3 -m py_compile src/solar_shift_router/dispatcher.py src/sovereign_jurisdiction_fence/fence.py src/handover_state_compiler/compiler.py src/jit_shift_authority_broker/custody.py src/merkle_handover_ledger/verifier.py

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
