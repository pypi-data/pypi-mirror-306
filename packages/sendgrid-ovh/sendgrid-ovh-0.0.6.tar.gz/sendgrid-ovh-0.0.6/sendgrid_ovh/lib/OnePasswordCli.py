import os
import subprocess


class OnePasswordCli:

    @staticmethod
    def has_proper_sendgrid_env_variables():
        return os.environ.get('ONEPASSWORD_SENDGRID_API_ID') is not None \
            and os.environ.get('ONEPASSWORD_SENDGRID_API_FOLDER') is not None \
            and os.environ.get('ONEPASSWORD_SENDGRID_API_ACCOUNT') is not None

    def get_sendgrid_secret(self, field):
        return self._get_secret(
            os.environ.get('ONEPASSWORD_SENDGRID_API_ACCOUNT'),
            os.environ.get('ONEPASSWORD_SENDGRID_API_FOLDER'),
            os.environ.get('ONEPASSWORD_SENDGRID_API_ID'),
            field
        )

    @staticmethod
    def has_proper_ovh_env_variables():
        return os.environ.get('ONEPASSWORD_OVH_ZONE_ID') is not None \
            and os.environ.get('ONEPASSWORD_OVH_ZONE_FOLDER') is not None \
            and os.environ.get('ONEPASSWORD_OVH_ZONE_ACCOUNT') is not None

    def _get_secret(self, account, folder, id, field ):
        code, out, error = self._op_cli("--account={} read -n op://{}/{}/{}".format(
            account,
            folder,
            id,
            field
        ))
        if code != 0:
            raise Exception('Unable to grab 1password secret field {}'.format(field))
        return out

    def get_ovh_secret(self, field):
        return self._get_secret(
            os.environ.get('ONEPASSWORD_OVH_ZONE_ACCOUNT'),
            os.environ.get('ONEPASSWORD_OVH_ZONE_FOLDER'),
            os.environ.get('ONEPASSWORD_OVH_ZONE_ID'),
            field
        )

    def _op_cli(self, cmd):
        """
        Call the 1Password cli (op)
        :param cmd: the op arguments and options
        :param inputstr: the input given to the command
        :return: A tuple of (returncode, stdout, stderr)
        """
        e = os.environ.copy()
        p = subprocess.Popen('op ' + cmd,
                             bufsize=0,
                             close_fds=True,
                             env=e,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE
                             )
        try:
            out, err = self._communicate(p)
        except subprocess.CalledProcessError:
            out = ''
            err = ''
        rc = p.returncode
        return rc, out.decode('utf-8'), err.decode('utf-8')

    @staticmethod
    def _communicate(subproc, inputstr=None):
        """
        Encode the input given to the subprocess if any
        :param subproc:
        :param inputstr:
        :return: A tuple of (stdout, stderr)
        """
        if inputstr is None:
            return subproc.communicate()
        if not inputstr:
            inputstr = ''
        return subproc.communicate(inputstr.encode())

