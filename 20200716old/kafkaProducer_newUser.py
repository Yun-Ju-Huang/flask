from confluent_kafka import Producer
import sys
import time

def to_kafka(m_id, data):
    # kafka
    props = {'bootstrap.servers': '35.201.205.44:9092'}
    producer = Producer(props)
    topicName = 'newUser'

    # data ##############################################################################################
    m_id = m_id             # 使用者的 m_id (PRIMARY KEY)
    m_name = data[0]        # 使用者的 姓名
    m_sex = data[1]         # 使用者 性別
    m_birthday = data[2]    # 使用者 生日日期
    m_height = data[3]      # 使用者 身高
    m_weight = data[4]      # 使用者 體重
    m_target = data[5]      # 使用者 飲食目標
    #####################################################################################################

    try:
        keyy = 'newUser'

        '''##############################################################
        預設格式：(照這樣填寫)
        kafka_msg = 'userID|sex|Birth|Height|Weight|target' 
        kafka_msg = 'M000099|1|19831014|172|89|tg01' 
        ###############################################################'''

        kafka_msg = f'{m_id}|{m_sex}|{m_birthday}|{m_height}|{m_weight}|{m_target}|'


        producer.produce(topicName, key=keyy, value=kafka_msg)
        producer.flush()
        print(f' ==> message sent to kafka : {kafka_msg}')
    except BufferError:
        sys.stderr.write('%% Local producer queue is full ({} messages awaiting delivery): try again\n'
                         .format(len(producer)))
    except Exception as e:
        print(e)

    producer.flush()