import importlib.util
from pathlib import Path
from Tasks_codes.Task3 import quantize_signal


# Helper function to dynamically load a Python file as a module
def load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Helper function to read input file into a dictionary
def load_input_signal(file_path):
    signal_dict = {}
    with open(file_path, "r") as f:
        lines = f.readlines()[3:]  # Skip header lines
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 2:
                signal_dict[float(parts[0])] = float(parts[1])
    return signal_dict


if __name__ == "__main__":
    base_dir = Path(__file__).parent / "Task 3 testcases"

    # =========================================================================
    # TEST CASE 1
    # =========================================================================
    print("--- Running Test Case 1 ---")
    test1_dir = base_dir / "Test 1"
    # Note: Rename "QuanTest1.py" below to "QuanTest.py" if that is your file's exact name
    quan_test1 = load_module("QuanTest1", test1_dir / "QuanTest1.py")

    input1_file = test1_dir / "Quan1_Input.txt"
    output1_file = test1_dir / "Quan1_Out.txt"

    # Load input & execute quantization
    input_sig1 = load_input_signal(input1_file)
    q_sig1, err_sig1, enc_sig1, lvl_idx1, delta1 = quantize_signal(
        input_sig1, bits=3
    )

    # Convert output dicts to lists for QuanTest1
    enc1_vals = list(enc_sig1.values())
    quant1_vals = list(q_sig1.values())

    # Run QuanTest1
    quan_test1.QuantizationTest1(str(output1_file), enc1_vals, quant1_vals)

    print("\n" + "=" * 50 + "\n")

    # =========================================================================
    # TEST CASE 2
    # =========================================================================
    print("--- Running Test Case 2 ---")
    test2_dir = base_dir / "Test 2"
    quan_test2 = load_module("QuanTest2", test2_dir / "QuanTest2.py")

    input2_file = test2_dir / "Quan2_Input.txt"
    output2_file = test2_dir / "Quan2_Out.txt"

    # Load input & execute quantization
    input_sig2 = load_input_signal(input2_file)
    q_sig2, err_sig2, enc_sig2, lvl_idx2, delta2 = quantize_signal(
        input_sig2, levels=4
    )

    # Convert output dicts to lists for QuanTest2
    lvl2_indices = list(lvl_idx2.values())
    enc2_vals = list(enc_sig2.values())
    quant2_vals = list(q_sig2.values())
    err2_vals = list(err_sig2.values())

    # Run QuanTest2
    quan_test2.QuantizationTest2(
        str(output2_file), lvl2_indices, enc2_vals, quant2_vals, err2_vals
    )