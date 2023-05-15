# Pendoc

Pendoc is a command-line tool for managing and documenting penetration testing activities. It provides a structured way to store and organize information related to targets, actions, vulnerabilities, and more.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<username>/pendoc.git

2. Navigate to the project directory:
   ```bash
    cd pendoc

3. Install the required dependencies:

   ```bash
    pip install -r requirements.txt

## Usage

1. Run the script:

   ```bash
    python pendoc.py

2. Follow the prompts to perform various actions such as creating a new session, adding targets, recording actions, etc.

## Features


 *   Create and manage multiple sessions for different engagements.
 *   Add targets with relevant information such as IP address, operating system, domain, etc.
 *   Record actions performed during the engagement, including commands executed, output, screenshots, etc.
 *   Keep track of vulnerabilities discovered, including CVE numbers, affected services, descriptions, and URLs.
 *   Add comments and notes to provide additional context or details.
 *   Easily copy relevant information to the clipboard for further use.
 *   Capture and save screenshots automatically.

## Configuration

Pendoc uses a configuration file (data2.conf) to store user-specific settings. By default, the file is located in the .config/pendoc directory. If the file doesn't exist, it will be created with default values.

## Folder Structure

Pendoc creates a folder structure to organize sessions, notes, images, scripts, and other files. The structure is as follows:


.
├── nmap
├── images
├── scripts
├── others


The nmap folder stores Nmap scan results, the images folder contains captured screenshots, the scripts folder holds custom scripts, and the others folder can be used to store additional files related to the engagement.


Please make sure to replace `<username>` with your actual GitHub username in the clone command.

