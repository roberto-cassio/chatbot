import html
import re


class InputSanitization:
  @staticmethod
  def sanitize_input(message):
    message = InputSanitization.remove_html_tags(message)
    message = InputSanitization.remove_control_chars(message)
    message = InputSanitization.truncate_text(message)

    return message

  @staticmethod
  def remove_html_tags(message):
    message = re.sub(r'<.*?>', '', message)
    message = html.escape(message)
    return message

  @staticmethod
  def remove_control_chars(text):
    return ''.join(c for c in text if c.isprintable())

  @staticmethod
  def truncate_text(text, max_length=1000):
    return text[:max_length]
