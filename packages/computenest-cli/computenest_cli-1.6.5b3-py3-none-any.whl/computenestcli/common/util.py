import re
import time
import yaml
import base64
import datetime
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
class Util:
    def __init__(self):
        pass

    @staticmethod
    def regular_expression(data):
        match = re.match(r'\$\{([\w\.]+)\}', data)
        if match:
            parts = match.group(1).split('.')
            return parts
        else:
            return None

    @staticmethod
    def add_timestamp_to_version_name(data=''):
        current_time = datetime.datetime.now()
        time_str = current_time.strftime("%Y%m%d%H%M%S")
        if data:
            new_version_name = str(data) + "_" + time_str
        else:
            new_version_name = time_str
        return new_version_name

    @staticmethod
    def lowercase_first_letter(data):
        if isinstance(data, dict):
            return {k[0].lower() + k[1:]: v for k, v in data.items()}
        elif isinstance(data, str):
            return data[0].lower() + data[1:]
        else:
            return data

    @staticmethod
    def run_cli_command(command, cwd):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=cwd)
        for line in iter(process.stdout.readline, b''):
            logger.info(line.decode().strip())
        output, error = process.communicate()
        return_code = process.returncode
        if return_code != 0:
            error = process.stderr.read().decode().strip()
            logger.error(error)
            raise ValueError(f"Shell command:{command} exec failed")
        return output, error

    @staticmethod
    def run_cli_commands(commands, cwd):
        for command in commands:
            logger.info(f"Executing command: {command}")
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, text=True, bufsize=1)

            for line in iter(process.stdout.readline, ''):
                logger.info(line.strip())
            stderr_output = process.stderr.read()

            process.stdout.close()
            process.stderr.close()
            return_code = process.wait()  # Wait for the process
            if return_code != 0:
                if stderr_output:
                    logger.error(stderr_output.strip())
                raise ValueError(f"Command '{command}' failed with return code {return_code}")

    @staticmethod
    def measure_time(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"\nExecution time: {int(execution_time)}s\n")
            return result

        return wrapper

    @staticmethod
    def get_current_time():
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return current_time

    @staticmethod
    def decode_base64(encoded_data):
        decoded_bytes = base64.b64decode(encoded_data)
        decoded_text = decoded_bytes.decode("utf-8")
        return decoded_text

    @staticmethod
    def write_yaml_to_file(data, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, allow_unicode=True)
