# _*_ encode:utf-8 _*_

from email.mime.multipart import MIMEMultipart

from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.audio import MIMEAudio
from email.mime.text import MIMEText
from email.encoders import encode_base64
import mimetypes
import os

from smail.configs import smtp_cfg


def get_conf(name):
    if name in smtp_cfg:
        return smtp_cfg[name]
    return False


def check_type(_type, *args):
    for arg in args:
        if not isinstance(arg, _type):
            raise TypeError('Parameter {} must be {}'.format(arg, _type))


def set_type(args):
    if not isinstance(args, (list, tuple)):
        return [args]
    return args


def get_abs_path(file):
    """if the file exists, return its abspath or raise a exception."""
    if os.path.isfile(file):
        return file
    else:
        raise Exception("The file %s doesn't exist." % file)


def _get_attachment_part(file):
    """According to file-type return a prepared attachment part."""
    name = os.path.split(file)[1]
    file_type = mimetypes.guess_type(name)[0]

    if file_type is None:
        print('Could not guess %s type, use application type instead.', file)
        file_type = 'application/octet-stream'

    main_type, sub_type = file_type.split('/')

    if main_type == 'text':
        with open(file, 'r') as f:
            part = MIMEText(f.read())
            part['Content-Disposition'] = 'attachment;filename="%s"' % name

    elif main_type in ('image', 'audio'):
        with open(file, 'rb') as f:
            part = MIMEImage(f.read(), _subtype=sub_type) if main_type == 'image' else \
                MIMEAudio(f.read(), _subtype=sub_type)
            part['Content-Disposition'] = 'attachment;filename="%s"' % name
    else:
        with open(file, 'rb') as f:
            part = MIMEBase(main_type, sub_type)
            part.set_payload(f.read())
            part['Content-Disposition'] = 'attachment;filename="%s"' % name
            encode_base64(part)

    return part


def mail_encode(message):

    check_type(dict, message)

    msg = MIMEMultipart()

    for k, v in message.items():
        if k.capitalize() in ('Subject',) and v:
            msg[k.capitalize()] = v

    if "content" in message:
        msg.attach(MIMEText('{}'.format(message['content']), 'plain', 'utf-8'))
    elif 'content_html' in message:
        msg.attach(MIMEText('{}'.format(message['content_html']), 'html', 'utf-8'))

    if 'attachments' in message and message['attachments']:
        attachments = set_type(message['attachments'])
        for attachment in attachments:
            attachment = get_abs_path(attachment)
            part = _get_attachment_part(attachment)
            msg.attach(part)

    return msg
