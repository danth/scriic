import os.path
import re

from .substitute import substitute_variables


class ScriicSyntaxException(Exception):
    pass

class MetadataException(Exception):
    pass

class MissingMetadataException(MetadataException):
    pass

class InvalidMetadataException(MetadataException):
    pass

class MissingParamException(Exception):
    pass


class FileRunner:
    def __init__(self, file_path):
        """
        Runner for a Scriic file.

        :param file_path: Path to the file to run.
        """
        self.file_path = file_path
        self.dir_path = os.path.dirname(file_path)

        self.code_begins_at = self._get_meta() + 1

    def _get_meta(self):
        """
        Read the metadata from the start of the code and prepare to run.

        :returns: Line number metadata ends on
        """
        self.title = None

        with open(self.file_path) as file:
            for line_no, line in enumerate(file):
                line = line.strip()

                if line.startswith('HOWTO '):
                    if self.title is None:
                        # Store the HOWTO text as the title
                        self.title = line[6:]
                    else:
                        raise InvalidMetadataException(
                            f'{self.file_path} has more than one HOWTO line')

                else:
                    if len(line) > 0:
                        # This must be a code line
                        line_no -= 1
                        break

        # Check that we got all required data
        if self.title is None:
            raise MissingMetadataException(
                f'{self.file_path} does not begin with a HOWTO line')

        # Create a list of required parameters based on the title
        self.params = list()
        for param in re.finditer(r'<(.+?)>', self.title):
            self.params.append(param.group(1))

        # Return the line metadata stopped at
        return line_no

    def run(self, params=None):
        """
        Run the code and return generated steps.

        :param params: Dictionary of parameters to pass to the script
        :returns: List of steps as strings
        """
        self.steps = list()
        self.sub_runner = None
        if params:
            self.variables = params.copy()
        else:
            self.variables = dict()

        # Check that all parameters have been set
        for param in self.params:
            if not param in self.variables:
                raise MissingParamException(
                    f'{self.file_path} is missing parameter {param}')

        # Run the script
        with open(self.file_path) as file:
            for line_no, line in enumerate(file):
                self._run_line(line, line_no)

        # Check for unfinished SUBs
        if self.sub_runner is not None:
            raise ScriicSyntaxException('Unfinished SUB')

        return self.steps

    def _run_line(self, line, line_no):
        """
        Run one line of code.

        :param line: Text of this line
        :param line_no: Position of this line in the file
        """
        if line_no < self.code_begins_at:
            return  # Skip metadata

        line = line.strip()
        if len(line) == 0:
            return  # This is a blank line, skip it

        if line.startswith('DO '):
            step = substitute_variables(line[3:], self.variables)
            self.steps.append(step)

        elif line.startswith('SET '):
            match = re.match(r'SET (.+) DOING (.+)', line)
            if not match:
                raise ScriicSyntaxException(line)

            # Create a step and get its index
            self.steps.append(match.group(2))
            # Set the variable to textually reference this step
            result_ref = f'the result of step {len(self.steps)}'
            self.variables[match.group(1)] = result_ref

        elif line.startswith('SUB '):
            sub_path = os.path.join(self.dir_path, line[4:])
            self.sub_runner = FileRunner(sub_path)

            if len(self.sub_runner.params) == 0:
                # This subscriic takes no parameters, run it now
                steps = self.sub_runner.run()
                self.steps.extend(steps)

                self.sub_runner = None
            else:
                self.sub_params = dict()

        elif line.startswith('WITH '):
            match = re.match(r'WITH (.+) AS (.+)', line)
            if not match:
                raise ScriicSyntaxException(line)

            param = substitute_variables(match.group(1), self.variables)
            self.sub_params[match.group(2)] = param

        elif line == 'GO':
            if self.sub_runner is None:
                raise ScriicSyntaxException('Unexpected GO')

            steps = self.sub_runner.run(self.sub_params)
            self.steps.extend(steps)

            self.sub_runner = None
            del self.sub_params

        else:
            raise ScriicSyntaxException(line)
