############ 使用私钥 - 公钥对信息进行"签名" + "验签" ##############
'''
作用：对解密后的文件的完整性、真实性进行验证（繁琐但更加保险的做法，很少用到）
应用场景：
    A有一私密文件欲加密后发送给B，又担心因各种原因导致B收到并解密后的文件并非完整、真实的原文件（可能被篡改或丢失一部分），
    所以A在发送前对原文件进行签名，将[签名和密文]一同发送给B让B收到后用做一下文件的[解密 + 验签],
    均通过后-方可证明收到的原文件的真实性、完整性。
    
'''
def to_sign_with_private_key(plain_text):
 
    #私钥签名
    signer_pri_obj = sign_PKCS1_v1_5.new(RSA.importKey(my_private_key))
    rand_hash = Hash.SHA256.new()
    rand_hash.update(plain_text.encode())
    signature = signer_pri_obj.sign(rand_hash)
 
    return signature
 
def to_verify_with_public_key(signature, plain_text):
 
    #公钥验签
    verifier = sign_PKCS1_v1_5.new(RSA.importKey(my_public_key))
    _rand_hash = Hash.SHA256.new()
    _rand_hash.update(plain_text.encode())
    verify = verifier.verify(_rand_hash, signature)
 
    return verify #true / false
 
def executer_with_signature():
 
    #签名/验签
    text = "I love CA!"
    assert to_verify_with_public_key(to_sign_with_private_key(text), text)
    print("rsa Signature verified!")
 
 
if __name__ == '__main__' :
 
    executer_without_signature() # 只加密不签名
 
    executer_with_signature()  #只签名不加密
 
    #二者结合食用更佳
'''
如果是加密的同时又要签名，这个时候稍微有点复杂。
1、发送者和接收者需要各持有一对公私钥，也就是4个钥匙。
2、接收者的公私钥用于机密信息的加解密
3、发送者的公私钥用于机密信息的签名/验签
4、接收者和发送者都要提前将各自的[公钥]告知对方。
'''

