# Hillclimb EV
Contains all sub-repos contributing to the Hillclimb EV project.

## Cloning

This project uses submodules. Make sure you fetch submodules when you clone and pull.

`git clone URL --recurse-submodules`

`git pull --recurse-submodules`

## Project Structure

* `docs` Top level documentation. More docs can be found throughout sub-project repos.
* `firmware` Software running directly on microcontrollers in the vehicle
  * `vcu` Vehicle Control Unit (VCU) target firmware
  * `vcu-proto` Prototype VCU firmware for evaluating prototype VCU hardware.
  * `inverter-proto` Prototype inverter firmware for evaluating prototype inverter hardware.
  * `control-lib` Implementation of Field Oriented Control for inverter motor control.
  * `system-lib` Common system firmware library. Code common to all STM32 microcontroller targets.
* `hardware` Hardware designs for custom hardware used in the vehicle
* `sim` Simulations (SIL and HIL) used to evalute the vehicle.
  * `powertrain_model` Simulink physical simulation of powertrain. SIL evaluation of inverter control firmware.
  * `hardwaresim` Embedded code to run on a BeagleBone to create a HIL environment for ECU hardware.
* `tools` Custom tools used for the vehicle.
  * `ecu-config` GUI tool for viewing and configuring ECU data over RS232.
