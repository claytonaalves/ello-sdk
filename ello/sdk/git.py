import os
import subprocess
import logging
import shutil

logger = logging.getLogger()


def git(args):
    cmd = 'git {0}'.format(args)
    with open(os.devnull, 'w') as FNULL:
        exit_code = subprocess.call(cmd, stdout=FNULL, stderr=subprocess.STDOUT)
    return exit_code


def create_version_tag(tag_name):
    logger.info("Criando tag {}".format(tag_name))
    git("tag {0}".format(tag_name))


def push_tags():
    logger.info("Enviando atualizações para o repositório remoto (commits, tags)...")
    git("push")
    git("push --tags")


def get_latest_tag():
    """ Get last defined tag from git log
    """
    cmd = 'git rev-list --tags --max-count=1'
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    last_hash = p.communicate()[0].strip()

    cmd = 'git describe --tags {}'.format(last_hash.decode('latin1'))
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    return p.communicate()[0].strip().decode('latin1')


def get_changes_from(from_tag):
    """ Retorna uma lista com as mensagens no formato:
        ['- msg <author>', '- msg <author>', ...]
    """
    cmd = ['git', 'log', '--reverse', '--first-parent', '--no-merges', '--pretty=format:%B-> author: <%an>', '{}..'.format(from_tag)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    git_output = p.communicate()[0].splitlines()
    git_output = map(lambda text: text.decode('utf8'), git_output)
    
    # Coleta apenas a primeira linha da mensagem, ignorando as linhas adicionais.
    changes = []
    try:
        while True:
            message = next(git_output)
            author = ''
            while author == '':
                tmp_line = next(git_output)
                if tmp_line.startswith('-> author: '):
                    author = ' '.join(tmp_line.split()[2:])
            changes.append('- {} {}'.format(message, author))
    except StopIteration:
        pass
    
    return changes


def install_hooks(args):
    """ Instala alguns hooks no repositorio atual """
    if not os.path.exists(".git"):
        print("Repositório git não encontrado")
        return
    hooks_path = os.path.abspath(os.path.dirname(__file__) + "/../../git_hooks")
    for root, dirs, files in os.walk(hooks_path):
        for filename in files:
            shutil.copyfile(os.path.join(hooks_path, filename), ".git/hooks/" + filename)