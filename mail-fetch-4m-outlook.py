import imapclient
import pyzmail
import bs4
uname = '<your-email-address>>'
upass = '<your-password>'
outlook_server_url = 'your.mail.server.com'
outlook_server_port = 993
# conn = imapclient.IMAP4_TLS(outlook_server_url,outlook_server_port, None ,90)
with imapclient.IMAPClient(host='your.mail.server.com',port=993) as client:
    client.login(uname, upass)
    inbox_folder = client.select_folder('INBOX', readonly=True)
    for key,value in inbox_folder.items():
        print('KEY => ',key,' Value => ',value)
        print('type-KEY => ',type(key),' type-Value => ',type(value))
        print('---------------------------------------------------------------')
    unique_ids = client.search(['ALL'])
    print(type(unique_ids), unique_ids)
    raw_message = client.fetch([4609], ['BODY[]', 'FLAGS'])
    message = pyzmail.PyzMessage.factory(raw_message[4609][b'BODY[]'])
    # html = message.html_part.get_payload().decode(message.html_part.charset)
    # soup = bs4.BeautifulSoup(html, 'lxml')
    # link_elems = soup.select('a')
    # print("I m soup -> ",soup)
    print("########### MAIL MESSAGE -> Start <- ##################")
    print("message is below ..... ")
    print(message)
    print("########### MAIL MESSAGE -> End <- ##################")
    # print('%d messages in INBOX' % inbox_folder['EXISTS'])
    client.logout()
# print(conn)
