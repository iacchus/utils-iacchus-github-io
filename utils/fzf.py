from subprocess import Popen, PIPE

def wrapper(string, charset='utf-8', decode=True, strip=True):
    """Wrapper for fzf.

    Pipes `string` to fzf and returns response or None in case of error

    Args:
        string (bytes or str): Data to be sent to fzf stdin.
        charset (str): Charset used for converting `bytes` <-> `str`.
        decode (bool): Wether to decode fzf `bytes` response to `str`.
        strip (bool): Wether to strip newlines from fzf response.
    """

    str_to_pipe_in = bytes()

    if type(string) == bytes:
        str_to_pipe_in = string
    elif type(string) = str:
        str_to_pipe_in = string.encode(charset)
    else:
        return None

    fzf_proc = Popen('fzf', shell=True, stdin=PIPE, stdout=PIPE)
    output, err = fzf_proc.communicate(input=str_to_pipe_in)

    if decode:  # decode bytes to charset str
        output = output.decode(charset)

    if strip:  # strips newline from output
        output = output.strip()

    return output
