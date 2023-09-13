
import subprocess


def get_ip_from_file(file_path):
    """
    file content: ip: 127.0.0.1
    @param file_path:
    @return:
    """
    try:
        cmd = f"cat {file_path} | grep ip: | awk -F ': ' '{{print $2}}' | awk -F '}}' '{{print $1}}'"
        output = subprocess.check_output(cmd, shell=True)
        return output.strip()
    except Exception as e:
        print('get ip failed, {}'.format(e.args))
        return ''
