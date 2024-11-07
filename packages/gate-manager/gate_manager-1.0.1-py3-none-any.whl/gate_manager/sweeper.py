# -*- coding: utf-8 -*-
"""
Gate class to interface with the Nanonis system for reading and setting voltages.

Created on Wed Nov 06 10:46:06 2024
@author: Chen Huang <chen.huang23@imperial.ac.uk>
"""


from decimal import Decimal
from datetime import datetime
import time
import os
import matplotlib.pyplot as plt
from tqdm import tqdm

from .gate import Gate, GatesGroup


class Sweeper:
    def __init__(self, outputs=None, inputs=None, slew_rate=None, amplification=None, temperature=None, device=None):
        self.outputs = outputs
        self.inputs = inputs
        self.slew_rate = slew_rate
        self.amplification = amplification
        self.temperature = temperature
        self.device = device
        
        self.x_label = None
        self.y_label = None
        self.comments = None
        self.filename = None
        
        self.start_voltage = None
        self.end_voltage = None
        self.step = None
        
        self.voltage = None
        self.voltages = []
        self.current = None
        self.currents = []
        
        
    def set_x_label(self, gates_group):
        self.x_label =  " & ".join(line.label for gate in gates_group.gates for line in gate.lines)
        
    def set_y_label(self, gate):
        self.y_label = " & ".join(line.label for line in gate.lines)
        
    def set_filename(self):
        current_dir = os.getcwd()
        self.filename = f"{self.temperature}_[{self.y_label}]_vs_[{self.x_label}]"
        if self.comments is not None:
            self.filename = self.filename + '_' + self.comments
        filepath = os.path.join(current_dir, self.filename)
        if os.path.isfile(filepath+'.txt'):
            counter = 2
            while os.path.isfile(f"{filepath}_run{counter}.txt"):
                counter += 1
            self.filename = f"{self.filename}_run{counter}"
        
    def log_params(self) -> None:
        """
        Log the parameters of the sweep to a file.

        Args:
            gates_out (GatesGroup): List of output gates that are being swept.
            gate_in (Gate): The input gate whose current is measured.
            start_voltage (Decimal): Starting voltage of the sweep.
            end_voltage (Decimal): End voltage of the sweep.
            step (Decimal): Step size for the sweep.
            filename (str): Name of the file where results are saved.
        """
        log_filename = "log"
        if self.comments is not None:
            log_filename += f"_{self.comments}"
        with open(f"{log_filename}.txt", 'a') as file:
            file.write(
                f"--- Run started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            file.write(f"{'Filename: ':>16} {self.filename}.txt \n")
            file.write(f"{'Device: ':>16} {self.device} \n")
            file.write(f"{'Amplifier: ':>16} {self.amplification} \n")
            file.write(f"{'Slew Rate: ':>16} {self.slew_rate} [V/s] \n")
            file.write(f"{'Swept Gates: ':>16} {self.x_label} \n")
            file.write(f"{'Measured Input: ':>16} {self.y_label} \n")
            file.write(f"{'Start Voltage: ':>16} {self.start_voltage:>24.16f} [V] \n")
            file.write(f"{'End Voltage: ':>16} {self.end_voltage:>24.16f} [V] \n")
            file.write(f"{'Step Size: ':>16} {self.step:24.16f} [V] \n")
            file.write("Initial Voltages of all outputs before sweep: \n")
            for output_gate in self.outputs.gates:
                file.write(
                    f"{output_gate.source.label:>16} {output_gate.voltage():>24.16f} [V] {" & ".join(line.label for line in output_gate.lines):>80} \n")
            file.write("\n")


    def sweep1D(self, swept_terminal: GatesGroup, measured_input: Gate, start_voltage: float, end_voltage: float, step: float, initial_state: list = None, comments: str = None) -> None:
        """
        Perform a 1D voltage sweep and create an animated plot of the measurement.

        Args:
            swept_terminal (GatesGroup): List of output gates to sweep over.
            measured_input (Gate): Gate used to measure the input voltage.
            start_voltage (float): Starting voltage value for the sweep.
            end_voltage (float): Ending voltage value for the sweep.
            step (float): Voltage increment for each step.
            initial_state (list): Initial voltage state for each gate in the setup.
        """
        # Define the file name
        self.set_x_label(swept_terminal)
        self.set_y_label(measured_input)
        self.comments = comments
        self.set_filename()
       
        
        self.start_voltage = Decimal(start_voltage)
        self.end_voltage = Decimal(end_voltage)
        self.step = Decimal(step)

        pbar = tqdm(total=len(self.outputs.gates)+len(swept_terminal.gates),  desc="[INFO] Ramping voltage", ncols=80, leave=True)
        
        idle_gates = []
        for gate in self.outputs.gates:
            if gate not in [state[0] for state in initial_state]:
                idle_gates.append(gate)
        GatesGroup(idle_gates).turn_off()
        pbar.update(len(idle_gates))

        for gate, initial_voltage in initial_state:
            gate.voltage(initial_voltage, False)

        # Wait for initial voltages to stabilize
        while not all([gate.is_at_target_voltage(voltage) for gate, voltage in initial_state]):
            time.sleep(0.1)
        pbar.update(len(initial_state))

        # Initialize sweep parameters and plotting
        swept_terminal.voltage(start_voltage)
        pbar.update(len(swept_terminal.gates))

        pbar.close()
        time.sleep(1)

        fig, ax = plt.subplots()
        line, = ax.plot([], [])
        ax.set_xlabel(f"{self.x_label} [V]")
        ax.set_ylabel(f"{self.y_label} [uA]")
        
        self.voltages, self.currents = [], []
        self.voltage = self.start_voltage

        # record the parameters
        self.log_params()

        # actually start the measurement
        print(
            f"[INFO] Start sweeping {self.x_label} from {float(self.start_voltage)} [V] to {float(self.end_voltage)} [V]. ")
        
        with open(f"{self.filename}.txt", 'a') as file:
            file.write(f"{self.x_label+' [V]':>24} {self.y_label+' [uA]':>24} \n")

        # Execute sweep and record data
        total = int(abs(self.end_voltage - self.start_voltage) / self.step + 1)
        pbar = tqdm(total=total, desc="[INFO] Sweeping",
                ncols=80, leave=True)  # progress bar
        frame = 0
        while True:
            swept_terminal.voltage(self.voltage)
            self.voltages.append(self.voltage)
            self.current = measured_input.read_current(self.amplification)
            self.currents.append(self.current)

            with open(f"{self.filename}.txt", 'a') as file:
                file.write(f"{self.voltage:>24.8f} {self.current:>24.16f} \n")
                
            ax.set_xlim(min(self.voltages) - self.step, max(self.voltages) + self.step)
            ax.set_ylim(min(self.currents) - Decimal(0.01),
                        max(self.currents) + Decimal(0.01))
            line.set_data(self.voltages, self.currents)
            plt.draw()
            plt.pause(0.1)
            frame += 1
            pbar.update(1)

            if (self.start_voltage < self.end_voltage and self.voltage > self.end_voltage - Decimal(1e-6)) or (
                    self.start_voltage > self.end_voltage and self.voltage < self.end_voltage + Decimal(1e-6)):
                pbar.close()
                break
            self.voltage = self.start_voltage + frame * \
                self.step if self.start_voltage < self.end_voltage else self.start_voltage - frame * self.step

        plt.savefig(f"{self.filename}.png", dpi=300)
        print("[INFO] Data collection complete and figure saved. \n")
        
        
    def sweep2D(self, X_swept_terminal: GatesGroup, X_start_voltage: float, X_end_voltage: float, X_step: float, 
                Y_swept_terminal: GatesGroup, Y_start_voltage: float, Y_end_voltage: float, Y_step: float,
                measured_input: Gate, initial_state: list, comments: str=None):
        
        Y_voltage = Y_start_voltage
        loop = 0
        params = {
             # here we use the variable name for the gate which is okay
             'swept_terminal': X_swept_terminal,
             'start_voltage': X_start_voltage,
             'end_voltage': X_end_voltage,
             'step': X_step,
             'measured_input': measured_input,
             'initial_state': initial_state,
             'comments': comments,
         }
        initial_state_basic = initial_state.copy()
        while True:
            initial_state = initial_state_basic.copy()
            for Y_gate in Y_swept_terminal.gates:
                initial_state.append([Y_gate, Y_voltage])
            params['initial_state'] = initial_state
            self.sweep1D(**params)
            loop += 1
            if (Y_start_voltage < Y_end_voltage and Y_voltage > Y_end_voltage - 1e-6) or (
                        Y_start_voltage > Y_end_voltage and Y_voltage < Y_end_voltage + 1e-6):
                break
            Y_voltage = Y_start_voltage + loop * Y_step if Y_start_voltage < Y_end_voltage else Y_start_voltage - loop * Y_step

