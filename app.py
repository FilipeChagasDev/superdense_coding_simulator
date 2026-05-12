import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from qiskit import QuantumCircuit
from qiskit.circuit import QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

CLASSICAL_OPTIONS = ["00", "01", "10", "11"]


@st.cache_resource
def get_simulator():
    """Cache the simulator instance to improve performance."""
    return AerSimulator()


def encode_alice_message(circuit: QuantumCircuit, qubit_index: int, selected_bits: str) -> None:
    if selected_bits == "01":
        circuit.z(qubit_index)
    elif selected_bits == "10":
        circuit.x(qubit_index)
    elif selected_bits == "11":
        circuit.z(qubit_index)
        circuit.x(qubit_index)


@st.cache_data
def build_superdense_coding_circuit(selected_bits: str, simulate_interceptor: bool) -> QuantumCircuit:
    qubit_b = QuantumRegister(1, "qb")
    qubit_a = QuantumRegister(1, "qa")
    receiver_bits = ClassicalRegister(2, "receiver")
    interceptor_bits = ClassicalRegister(1, "interceptor")
    qc = QuantumCircuit(qubit_a, qubit_b, receiver_bits, interceptor_bits)

    qc.h(qubit_a[0])
    qc.cx(qubit_a[0], qubit_b[0])
    qc.barrier()

    encode_alice_message(qc, qubit_a[0], selected_bits)

    if simulate_interceptor:
        qc.barrier()
        qc.measure(qubit_a[0], interceptor_bits[0])

    qc.barrier()
    qc.cx(qubit_a[0], qubit_b[0])
    qc.h(qubit_a[0])
    qc.barrier()
    qc.measure(qubit_a[0], receiver_bits[0])
    qc.measure(qubit_b[0], receiver_bits[1])

    return qc


def run_simulation(circuit: QuantumCircuit, shots: int):
    simulator = get_simulator()
    from qiskit_aer.primitives import SamplerV2
    sampler = SamplerV2(simulator)
    result = sampler.run((circuit,), shots=shots).result()
    return result[0].data


def counts_to_dataframe(counts: dict, shots: int) -> pd.DataFrame:
    df = pd.DataFrame(list(counts.items()), columns=["State", "Count"])
    df["Probability (%)"] = (df["Count"] / shots * 100).round(2)
    return df.sort_values("Count", ascending=False).reset_index(drop=True)


def render_about_section() -> None:
    st.expander("📚 About Superdense Coding", expanded=True).markdown(
        """
        **Superdense Coding** is a quantum communication protocol that enables transmitting **2 classical bits** 
        using only **1 quantum qubit** shared between two parties (Alice and Bob).

        **How it works:**
        1. **Bob** prepares an entangled quantum pair (Bell state) between **qubit A** and **qubit B**
        2. **Alice** receives qubit A and applies a unitary operation that encodes 2 classical bits (00, 01, 10, or 11)
        3. **Bob** performs a joint measurement (Bell measurement) on both qubits and recovers the 2 original bits

        **Bell States:** The protocol uses Bell states as the basis for the initial entanglement, 
        allowing a local operation by Alice on a single qubit to be encoded in a global state.

        **Protocol Security:**
        - **Eavesdropping Detection:** If an eavesdropper (Eve) measures qubit A before Bob, the entanglement is broken
        - **Quantum Collapse:** Any unauthorized measurement collapses the state, destroying the correlation needed for correct decoding
        - **No-Cloning Theorem:** Eve cannot copy the qubit to measure without leaving traces
        - **Guaranteed Detection:** If Eve intercepts, Bob will detect a significant error rate in the Bell measurement, revealing the eavesdropping

        **Applications:** Secure quantum communication protocols, quantum cryptography, and reliable quantum networks.
        """
    )


def render_controls() -> tuple[str, bool, int]:
    with st.container(border=True):
        st.write("**COMMUNICATION SETTINGS**")
        selected_bits = st.selectbox(
            "Select the classical bits that Alice should send to Bob:",
            options=CLASSICAL_OPTIONS,
            index=0,
        )
        simulate_interceptor = st.checkbox("Simulate Eve's eavesdropping")

    with st.container(border=True):
        st.write("**SIMULATION PARAMETERS**")
        n_shots = st.number_input(
            "Number of simulation shots",
            min_value=1,
            max_value=1000,
            value=100,
            step=1,
        )

    return selected_bits, simulate_interceptor, n_shots


def render_quantum_circuit(circuit) -> None:
    fig = circuit.draw("mpl", fold=100)
    st.write("**Generated Quantum Circuit:**")
    st.pyplot(fig)
    plt.close(fig)


def render_simulation_results(data, shots: int, simulate_interceptor: bool) -> None:
    with st.container(border=True):
        st.write("**SIMULATION RESULTS**")

        receiver_counts = data.receiver.get_counts()
        receiver_df = counts_to_dataframe(receiver_counts, shots)

        st.write("**Receiver's (Bob) Measurements:**")
        st.dataframe(receiver_df, use_container_width=True)

        if simulate_interceptor:
            interceptor_counts = data.interceptor.get_counts()
            interceptor_df = counts_to_dataframe(interceptor_counts, shots)

            st.write("**Eavesdropper's (Eve) Measurements:**")
            st.dataframe(interceptor_df, use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="Superdense Coding Simulator", layout="centered")
    st.title("Superdense Coding Simulator")
    st.write("**Developed By Filipe Chagas Ferraz (github.com/filipechagasdev)**")

    render_about_section()
    selected_bits, simulate_interceptor, n_shots = render_controls()

    circuit = build_superdense_coding_circuit(selected_bits, simulate_interceptor)
    render_quantum_circuit(circuit)

    if st.button("Simulate", use_container_width=True):
        data = run_simulation(circuit, n_shots)
        render_simulation_results(data, n_shots, simulate_interceptor)


if __name__ == "__main__":
    main()
