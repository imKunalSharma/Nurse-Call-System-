# Nurse-Call-System-
Nurse Call System Project code run on python

Nurse Call Monitoring and Alert System

Application: NTS-MDSOFT21 Ver1.2
Programming Language: Python
GUI Framework: PyQt5
Hardware Platform: Raspberry Pi

Introduction

The Nurse Call Monitoring and Alert System is a Python-based application developed to monitor patient-bed call conditions at a centralized nurse station. It communicates with a hardware controller through a serial interface and presents bed status information through a graphical user interface.

Objectives

Monitor configured beds and rooms in real time.

Receive and process controller status messages.

Distinguish normal calls, emergency calls, and Code Blue conditions.

Provide audible alerts and visual status indications.

Display the current date, time, wing name, and hospital identification.

Store controller status records in date-wise CSV files.

Maintain alert-room lists through INI configuration files.

System Design

The software consists of a PyQt5 monitoring interface, an asynchronous serial communication component, a GPIO control component, an alert-management component, and a file-based configuration and logging component.

Communication and Data Processing

The application communicates at 9600 baud. Incoming messages are collected until a carriage-return terminator is received. Valid messages are parsed to extract a controller identifier and status values. Controller-specific position mappings are then used to update the corresponding bed status entries.

Alert Management

The implementation processes status values 0, 1, 2, and 3 for cleared, normal-call, emergency-call, and Code Blue logic, respectively. Normal and emergency conditions use different buzzer patterns. Code Blue conditions update a room list stored in the shared configuration file.

Data Storage

The application reads configuration information from db.ini and updates alert-room information in my.ini. It creates date-wise and controller-wise folders and stores timestamped records in CSV files.

Hardware Integration

The application uses Raspberry Pi BCM GPIO 23 for buzzer control, GPIO 24 for the communication indicator output, and GPIO 25 for the physical switch input. Audio volume is managed through ALSA.

Conclusion

The project integrates a graphical monitoring interface with serial communication, GPIO control, alert handling, and CSV data logging. It provides a foundation for a centralized nurse-call monitoring application. Further testing of serial reliability, alert priorities, configuration validation, logging consistency, and safe hardware shutdown is recommended before production deployment.
