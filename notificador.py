#coding: utf8
""" Este script é responsável por efetuar a notificação de novos builds.
    Desta forma o time de HelpDesk é notificado imediatamente após
    o término da compilação e disponibilização do executável.
"""
import Skype4Py as skype
import config
import ello
import telegram

CHANGELOG_URL = "http://wiki.ellotecnologia.net.br/wiki:changelog"

def notifica_suporte_via_skype():
    print u'Notificando suporte sobre a nova versão...'
    versao = '.'.join(ello.versao_no_changelog())
    mensagem = (u"Versão {} disponível para atualização.\n\n"
                u"Informações sobre o que foi implementado/corrigido nesta versão\n"
                u"podem ser vistos no log de atualizações -> {}"
               ).format(versao, CHANGELOG_URL)

    try:
        client = skype.Skype()
        client.Attach()
        blob = config.skype_group_blob
        chat = client.CreateChatUsingBlob(blob)
        chat.SendMessage(mensagem)
    except skype.errors.SkypeAPIError:
        print "Falha ao notificar via skype..."

def notifica_suporte_via_whatsapp():
    versao = '.'.join(ello.versao_no_changelog())
    mensagem = "Nova revisao %s disponivel para download - Ello Tecnologia." % versao
    celular = "556692836044-1446577135" # Grupo Ello
    print 'Notificando %s via WhatsApp...' % celular
    envia_msg_whatsapp(celular, mensagem)

def envia_msg_whatsapp(numero_celular, mensagem):
    import requests
    #numero_celular = "55" + numero_celular
    payload = {'fone': numero_celular, 'msg': mensagem}
    r = requests.get(config.whatsapp_url, params=payload)

def notifica(skype=True, whatsapp=True):
    #if skype:
    #    notifica_suporte_via_skype()
    #if whatsapp:
    #    notifica_suporte_via_whatsapp()
    telegram.notifica()

if __name__=="__main__":
    notifica(True, True)

