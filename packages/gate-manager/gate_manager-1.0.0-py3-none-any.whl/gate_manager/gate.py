import time
from typing import Union
from nanonis_tramea import Nanonis
from decimal import Decimal
import time

from .connection import NanonisSource


class Gate:
    """
    A class representing a gate used in experiments interfacing with the Nanonis system.

    Attributes:
        name (str): The name of the gate.
        label (str): A label identifying the gate.
        read_index (int): The index used to read voltage from the gate.
        write_index (int, optional): The index used to write voltage to the gate (None if not writable).
        nanonisInstance (Nanonis): An instance of the Nanonis class for communication with the device.
    """

    def __init__(self, source: NanonisSource = None, lines: list[int] = None):
        """Initializes the Gate with its name, label, read/write indices, and the Nanonis instance."""
        self.source = source
        self.lines = lines
        self.label = "&".join(line.label for line in self.lines)
        self.nanonisInstance = self.source.nanonisInstance
        self._voltage = self.get_volt()

    def verify(self, target_voltage) -> None:
        min_voltage = -2
        max_voltage = 2
        if target_voltage < min_voltage or target_voltage > max_voltage:
            raise ValueError(
                f"{self.label} target voltage {target_voltage} is out of range {(min_voltage, max_voltage)}.")

    def set_volt(self, target_voltage: Union[float, Decimal]) -> None:
        """Sets the voltage for the gate, raises error if gate is read-only."""
        self.verify(target_voltage)
        if self.source.write_index is None:
            raise ValueError(
                f"'{self.label}' cannot set voltage because write_index is not defined.")
        else:
            self.nanonisInstance.UserOut_ValSet(self.source.write_index, Decimal(target_voltage))

    def get_volt(self) -> Decimal:
        """Retrieves the current voltage from the gate."""
        self._voltage = Decimal(self.nanonisInstance.Signals_ValsGet([self.source.read_index], True)[2][1][0][0])
        return self._voltage

    def voltage(self, target_voltage: Union[float, Decimal] = None, is_wait: bool = True) -> Decimal:
        """Gets or sets the voltage. If no value is provided, it reads the current voltage."""
        if target_voltage is None:
            self.get_volt()
            return self._voltage
        else:
            self.set_volt(target_voltage)
            if is_wait:
                while not self.is_at_target_voltage(target_voltage):
                    time.sleep(0.1)

    def turn_off(self, is_wait: bool = True):
        """Sets the gate voltage to zero."""
        self.voltage(0.0, is_wait)

    def is_at_target_voltage(self, target_voltage: Union[float, Decimal],
                             tolerance: Union[float, Decimal] = 1e-6) -> bool:
        """Check if the current voltage is within tolerance of the target."""
        self.get_volt()
        return abs(self._voltage - Decimal(target_voltage)) < Decimal(tolerance)

    def read_current(self, amplification: float = -10 ** 6) -> Decimal:
        """Reads the current from the gate, adjusted by the amplifier setting."""
        return Decimal(
            self.nanonisInstance.Signals_ValGet(self.source.read_index, True)[2][0] * 10 ** (6) / amplification)


class GatesGroup:
    """A class to manage a group of gates, allowing simultaneous control of multiple gates."""

    def __init__(self, gates: list[Gate]):
        """Initializes the group with a list of Gate instances."""
        self.gates = gates

    def add(self, gate) -> None:
        """Adds a gate to the group."""
        self.gates.append(gate)

    def set_volt(self, target_voltage: Union[float, Decimal]) -> None:
        """Sets the voltage of all gates in the group to a target value."""
        for gate in self.gates:
            gate.set_volt(target_voltage)

    def voltage(self, target_voltage: Union[float, Decimal], is_wait: bool = True) -> None:
        """Sets or retrieves the voltage for all gates in the group."""
        for gate in self.gates:
            gate.voltage(target_voltage, False)
        if is_wait:
            # print(f"[INFO] Ramping {[gate.label for gate in self.gates]} to {target_voltage} [V]. ")
            while not all(gate.is_at_target_voltage(target_voltage) for gate in self.gates):
                time.sleep(0.1)
            # print(f"[INFO] {[gate.label for gate in self.gates]} is at {target_voltage} [V]. ")

    def turn_off(self, is_wait: bool = True) -> None:
        """Turns off all gates in the group by setting their voltages to zero."""
        self.voltage(0.0, is_wait)
