from homework.setup_logger import err_logger, info_logger, log
import re
import csv
# import time

class Patient:

    # __slots__ = ('first_set', '__first_name', '__last_name', 'birth_date', 'phone', 'document_type', 'document_id')

    def __init__(self, *args) -> None:
        '''Constructor'''

        if len(args) == 6:
            self.first_set = 0
            self.birth_date = args[2]
            self.phone = args[3]
            self.document_type = args[4]
            self.document_id = args[5]
            self.first_name = args[0]
            self.last_name = args[1]
            print(f"Patient {self.first_name} {self.last_name} created")
            with log():
                info_logger.info(f"Patient {self.first_name} {self.last_name} created with attributes: " +
                    f"birth date: {self.birth_date} " +
                    f"phone: {self.phone} " +
                    f"document_type: {self.document_type} " +
                    f"document_id: {self.document_id}")
        else:
            with log():
                err_logger.error('AttributeError: Wrong number of params')
            raise AttributeError('Wrong number of params')



    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.birth_date} {self.phone} {self.document_type} {self.document_id}"


    @property
    def first_set(self):
        return self.__first_set

# Как еще можно сделать запрет на увеличение значения first_set извне?
    @first_set.setter
    def first_set(self, value):

        if not hasattr(self, 'first_set'):
            self.__first_set = 0
        elif self.first_set < 2:
            self.__first_set += 1
        else:
            with log():
                err_logger.error(f"ValueError: Cannot reset value of first_set: {self.first_set}")
            raise ValueError(f"ValueError: Cannot reset value of first_set: {self.first_set}")


    @property
    def first_name(self):

        return self.__first_name


    @first_name.setter
    def first_name(self, first_name):

        if self.first_set < 2:

            if not isinstance(first_name, str):
                with log():
                    err_logger.error("TypeError: Invalid name type, should be str")
                raise TypeError("TypeError: Invalid name type, should be str")

            if first_name.strip().isalpha():
                self.__first_name = first_name.capitalize()
                self.__first_set += 1
            else:
                with log():
                    err_logger.error(f"ValueError: Invalid first name: {first_name}")
                raise ValueError(f"ValueError: Invalid first name: {first_name}")
        else:
            with log():
                err_logger.error(f'AttributeError: Cannot reset first name of {self.first_name} {self.last_name}')
            raise AttributeError(f'AttributeError: Cannot reset first name of {self.first_name} {self.last_name}')


    @property
    def last_name(self):

        return self.__last_name


    @last_name.setter
    def last_name(self, last_name):

        if self.first_set < 2:

            if not isinstance(last_name, str):
                with log():
                    err_logger.error("TypeError: Invalid name type, should be str")
                raise TypeError("TypeError: Invalid name type, should be str")

            if last_name.strip().isalpha():
                self.__last_name = last_name.capitalize()
                self.__first_set += 1

            else:
                with log():
                    err_logger.error(f"ValueError: Invalid last name: {last_name}")
                raise ValueError(f"ValueError: Invalid last name: {last_name}")
        else:
            with log():
                err_logger.error(f'AttributeError: Cannot reset last name of {self.first_name} {self.last_name}')
            raise AttributeError(f'AttributeError: Cannot reset last name of {self.first_name} {self.last_name}')


    @property
    def birth_date(self):

        return self.__birth_date


    @birth_date.setter
    def birth_date(self, birth_date):

        if not isinstance(birth_date, str):
            with log():
                err_logger.error("TypeError: Invalid birth date type, should be str")
            raise TypeError("TypeError: Invalid birth date type, should be str")

        pattern_one = re.compile(r'(18|19|20)\d\d.(0[1-9]|1[012]).(0[1-9]|[12][0-9]|3[01])')
        pattern_two = re.compile(r'(0[1-9]|[12][0-9]|3[01]).(0[1-9]|1[012]).(18|19|20)\d\d')
        birth_date = birth_date.strip()
        if re.fullmatch(pattern_one, birth_date):
            self.__birth_date = birth_date[:4]+'-'+birth_date[5:7]+'-'+birth_date[8:]
        elif re.fullmatch(pattern_two, birth_date):
            self.__birth_date = birth_date[6:]+'-'+birth_date[3:5]+'-'+birth_date[:2]
        else:
            with log():
                err_logger.error(f"ValueError: Invalid birth date format: {birth_date}")
            raise ValueError(f"ValueError: Invalid birth date format: {birth_date}")

        if self.first_set > 0:
            with log():
                info_logger.info(f"Birth date was reset for {self.first_name} {self.last_name}")


    @property
    def phone(self):

        return self.__phone

    @phone.setter
    def phone(self, phone):

        if not isinstance(phone, str):
            with log():
                err_logger.error("TypeError: Invalid phone type, should be str")
            raise TypeError("TypeError: Invalid phone type, should be str")

        pattern = re.compile('[^0-9]')
        phone = ''.join([re.sub(pattern, "", symbol) for symbol in phone])
        if not len(phone) == 11:
            with log():
                err_logger.error(f"ValueError: Invalid phone number length: {phone}")
            raise ValueError(f"ValueError: Invalid phone number length: {phone}")

        if phone.startswith('8') or phone.startswith('7'):
            self.__phone = '+7-'+phone[1:4]+'-'+phone[4:7]+'-'+phone[7:9]+'-'+phone[9:]
        else:
            with log():
                err_logger.error(f"ValueError: Invalid phone number format: {phone}")
            raise ValueError(f"ValueError: Invalid phone number format: {phone}")

        if self.first_set > 0:
            with log():
                info_logger.info(f"Phone was reset for {self.first_name} {self.last_name}")


    @property
    def document_type(self):

        return self.__document_type


    @document_type.setter
    def document_type(self, doc_type):
        passport = ['паспорт', 'пасспорт']
        foreign = ['загран', 'заграничныйпаспорт', 'загранпаспорт']
        license = ['права', 'водительскиеправа', 'водительскоеудостоверение']

        if not isinstance(doc_type, str):
            with log():
                err_logger.error("TypeError: Invalid document type, should be str")
            raise TypeError("TypeError: Invalid document type, should be str")
        doc_type = doc_type.strip().replace(' ', '')

        if doc_type.lower() in passport:
            self.__document_type = 'Паспорт'
        elif doc_type.lower() in foreign:
            self.__document_type = 'Заграничный паспорт'
        elif doc_type.lower() in license:
            self.__document_type = 'Водительские права'
        else:
            with log():
                err_logger.error(f"ValueError: Cannot identify the document type: {doc_type}")
            raise ValueError(f"ValueError: Cannot identify the document type: {doc_type}, try: 'паспорт', 'загран', 'права'")

        if self.first_set > 0:
            with log():
                info_logger.info(f"Document type was reset for {self.first_name} {self.last_name}")    


    @property
    def document_id(self):

        return self.__document_id


    @document_id.setter
    def document_id(self, doc_id):

        if not isinstance(doc_id, str):
            with log():
                err_logger.error("Invalid document id, should be str")
            raise TypeError("Invalid document id, should be str")

        pattern = re.compile('[^0-9]')
        doc_id = ''.join([re.sub(pattern, "", symbol) for symbol in doc_id])
        # doc_id = doc_id.strip().replace(' ', '')

        if self.document_type == 'Паспорт' or self.document_type == 'Водительские права':
            length = 10
            space_id = 4
        elif self.document_type == 'Заграничный паспорт':
            length = 9
            space_id = 2
        else:
            with log():
                err_logger.error(f"ValueError: Cannot identify the document type: {self.document_type}")
            raise ValueError(f"ValueError: Cannot identify the document type: {self.document_type}")
        
        pattern = re.compile('([0-9]{'+str(length)+'})')
        if re.fullmatch(pattern, doc_id):
            self.__document_id = doc_id[:space_id]+' '+doc_id[space_id:]
        else:
            with log():
                err_logger.error(f"Invalid document id: {doc_id} for this document type - {self.document_type}")
            raise ValueError(f"Invalid document id: {doc_id} for this document type - {self.document_type}")

        if self.first_set > 0:
            with log():
                info_logger.info(f"Document id was reset for {self.first_name} {self.last_name}")    


    @staticmethod
    def create(first_name, last_name, birth_date, phone, document_type, document_id):
        return Patient(first_name, last_name, birth_date, phone, document_type, document_id)

    def save(self):
        try:
            with open('1.csv', 'a', encoding="utf8", newline='') as wf:
                fields = [self.first_name, self.last_name, self.birth_date,
                    self.phone, self.document_type, self.document_id]
                writer = csv.writer(wf)
                writer.writerow(fields)
            with log():
                info_logger.info(f"Patient saved: {' '.join(fields)}")
            print(f"Patient saved: {' '.join(fields)}")

        except Exception as e:
            with log():
                err_logger.error(e)
            print(e)


class PatientCollection:

    def __init__(self, csvfile):
        self.path = csvfile
        self.filePos = 0
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        rf = open(self.path, 'r', encoding='utf-8')
        rf.seek(self.filePos)
        data = rf.readline()
        self.filePos = rf.tell()
        rf.close()
        if not data:
            raise StopIteration
        self.counter += 1
        args = [*data.split(',')]

        return Patient(*args)

    def limit(self, counter):
        self.counter = counter
        return self.__iter__()

# obj1 = Patient.create("098098", "56876576558", "ABCDEF", "", "sdfsdfsdfs", "0000/000-000")
# print(obj1)
# obj1.first_name = "Василий"
# obj1.phone = "89061234567"
# obj1.save()

# collection = PatientCollection('1.csv')
# for patient in collection:
#     print(patient)
    # time.sleep(5)



