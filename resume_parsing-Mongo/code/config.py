data_new = "E:/ML/resume_parsing/data/new/"
data_prc = "E:/ML/resume_parsing/data/processed/"
data_path = "E:/ML/resume_parsing/data/"

doc_path = "E:/ML/resume_parsing/docs/"

graph_path = "E:/ML/resume_parsing/graphs/"

output_path = "E:/ML/resume_parsing/output/"

java_path = "C:/Program Files/Java/jdk-10.0.2/bin/java.exe"



# sftp connect 1
sftp_host = '182.72.41.26'
sftp_port = 22
sftp_username = 'root'
sftp_password = 'Auth@dm1n'

remote_path = '/home/calibehr/public_html/admin/upload/jobs/'

# sftp connect 2
# sftp_host = '172.16.1.75'
# sftp_port = 22
# sftp_username = 'root'
# sftp_password = 'St33p@2017'

# remote_path = '/virtualhost/narayanbhargavagroup.com/upload/jobs/'


# MongoDB Connect
mongo_host = "172.16.1.70"
# mongo_username = "calibehr/anevrekar"
# mongo_password = "Tomato@1234"


### Add words that are not names but identified as names by Stanfords NER
 
not_names = ['navi', 'mumbai', 'vitae', 'resume', 'taluka', 'making', 'residency', 'apartments', 
             'vihar', 'nagar', 'sadan', 'talaw', 'khana', 'stream', 'polytechnic', 'soya', 'white',
             'date', 'gurukul', 'wilmer', 'chowk', 'bogda', 'master', 'curriculum', 'mr', 'shri',
             'university', 'ultrasonic', 'village', 'institution', 'model', 'father', 'mother',
             'north', 'south', 'east', 'street', 'curriculam', 'email', 'phone', 'mobile', 'homes',
             'ghansoli', 'road', 'personal', 'data', 'mail', 'e', 'address', 'permanent', ]

building_names = ['residency', 'apartments', 'vihar', 'nagar', 'sadan', 'talaw', 'taluka', 'chowk', 'appartment',
                  'colony', 'bogda', 'village','street', 'homes', 'road', 'apt', ]



### Education Levels:
ssc = [' ssc ', ' s.s.c ', ' s.s.c. ','10th', 'high school' ]
hsc = [' hsc ', ' h.s.c ', ' h.s.c. ', '12th', 'intermediate']
diploma = [' diploma ']
engineering = [' b.e. ', ' b.e ', 'bachelor of engineering', ' b.tech ', ' b. tech ', 'bachelors of engineering',
               'civil', ' b. e ']
degree = [' b.sc ', ' b. sc ', ' bachelors ', 'b.com', ' b.a. ', ' bca ', ' b com ', ' bachelor ', 
          ' graduation ', ' graduated ', ' b.a ', 'bsc', 'b.sc.', 't.y.','b.sc ',
          'b.ed', 'b. ed']
post_grad = [' mba ', ' mca ', ' masters ', ' m.b.a. ', ' m.b.a ', 'm.com', ' m. com ', ' m.a ',
             'm.sc.', 'm.sc ' ]



