import base64
import sys

encode_path = "/home/eray/Documents/AUO_CIC/20210722_112342_End_00001.jpg"
save_path = "/home/eray/Documents/AUO_CIC/1081001.jpg"


def encode(path):
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read())
    
    return encoded


def decode(code):
    decoded = base64.b64decode(code)
    
    return decoded


def to_img(name, code):
    with open(name, "wb") as f:
        f.write(code)


if __name__ == "__main__":
    #for line in sys.stdin:
        #img = line.rstrip()
        #if len(img) == 0:
            #continue

        #print(encode(img))

    print(encode(encode_path).decode("utf-8"))
    #decode(encode(encode_path))

    #to_img(save_path, decode(encode(encode_path)))





