def show_menu():
    print('1. Распечатать справочник',
          '2. Найти телефон по фамилии',
          '3. Изменить контакт',
          '4. Удалить запись',
          '5. Найти абонента по номеру телефона',
          '6. Добавить абонента в справочник',
          '7. Скопировать контакт из другого справочника',
          '8. Сохранить изменения в справочнике',
          '9. Закончить работу', sep = '\n')
    choice=int(input("Введите номер команды: "))
    return choice

def read_txt(txt_file_name):
    result_list=[] 
    fields=['id','Фамилия', 'Имя', 'Телефон', 'Описание']
    data_txt=open(txt_file_name, 'r', encoding='utf-8')
    for line in data_txt:
        if line!='\n':
            result_list.append(dict(zip(fields, map(lambda x: x.strip(), line.split(','))))) 
    data_txt.close()
    return result_list

def print_contact(result_dict):
    for i in result_dict:
        for k,v in i.items():
            print (k,':',v)
        print()
     
def print_phonebook(phnb_lst):
    fields=['id:','Фамилия:', 'Имя:', 'Телефон:', 'Описание:']
    correct_size_for_print=lambda x,n:x+''.join([' ' for i in range(n-len(x))]) 
    for k in fields:
        print(f"{k.center(20)}", end='')
    print('\n')
    for i in phnb_lst:
        for k,v in i.items():
            if k!='id':
                print(correct_size_for_print(v,20),end='')
            else:
                print(correct_size_for_print(v,6),end='')
        print()
    print('\n')

def give_id_to_new_contact(phnb_lst):
    if len(phnb_lst)!=0:
        return str(max([int(i['id']) for i in phnb_lst])+1)
    else:
        return str(1)


def find_number_by_lastname(phnb_lst, last_name): 
    find_lst=[] 
    for i in phnb_lst:
        if i['Фамилия']==last_name:
            find_lst.append(i)
    if len(find_lst)!=0:
        if len(find_lst)>1:
            print("Найдено несколько контактов с такой фамилией\n")
            for c in find_lst:
                print(c['Фамилия'], c['Имя'], c['Телефон'])
        else:
            print(find_lst[0]['Телефон'])
    else:
        print('Контакта с такой фамилией нет')


def find_contact_index_for_changing(phnb_lst,last_name): 
    find_lst=[] 
    for i in range(len(phnb_lst)):
        if phnb_lst[i]['Фамилия']==last_name:
            find_lst.append(i)
    if len(find_lst)!=0:
        if len(find_lst)>1:
            print("Найдено несколько контактов с такой фамилией, необходимо уточнить id\n")
            print_contact([phnb_lst[cont_ind] for cont_ind in find_lst])
            id=input("Введите id для уточнения: ")
            not_find_id=True
            for cont_ind in find_lst:
                if phnb_lst[cont_ind]['id']==id:
                        return cont_ind
            if not_find_id:
               return 'Контакта с таким id нет'
        else:
            return find_lst[0]
    else:
        return 'Контакта с такой фамилией в отобранном списке нет'


def show_edit_menu():
    print('1. Фамилия',
          '2. Имя',
          '3. Телефон',
          '4. Описание',
          '5. Подтвердить изменения',
          '6. Отменить изменения', sep = '\n')  
    choice=int(input("Введите номер команды: "))
    return choice

def edit_contact(phnb_lst,last_name):
    cont_ind=find_contact_index_for_changing(phnb_lst,last_name)
    if type(cont_ind)==str:
        print(cont_ind) 
    else:
        print_contact([phnb_lst[cont_ind]])
        choice=show_edit_menu()
        fields=['Фамилия', 'Имя', 'Телефон', 'Описание']
        edit=False
        edited_contact=phnb_lst[cont_ind].copy()
        while choice not in [5,6]:
            k=fields[choice-1]
            new_data=input(f'{k}: ').strip().replace(',','')
            if k=='Телефон':
                if new_data!='' and new_data in [i['Телефон'] for i in phnb_lst]: 
                    exist_number_ind=[i['Телефон'] for i in phnb_lst].index(new_data)  
                    print("Контакт с таким номером уже существует!")
                    print_contact([phnb_lst[exist_number_ind]])
                    choice=show_edit_menu()
                    continue
            elif  k=='Фамилия':
                letter_symbols=[chr(i) for i in range(1040,1104)]+[chr(i) for i in range(65,91)]+[chr(i) for i in range(97,123)] 
                if set(new_data)&set(letter_symbols)==set():
                    print("Поле 'Фамилия' обязательно для заполнения и должно содержать буквенные символы")
                    choice=show_edit_menu()
                    continue
            edited_contact[k]=new_data
            edit=True
            choice=show_edit_menu()
        if choice==5 and edit==True:
            print("Контакт изменен")
            phnb_lst[cont_ind]=edited_contact
            print_contact([phnb_lst[cont_ind]])
            

def delete_by_lastname(phnb_lst,last_name):
    cont_ind=find_contact_index_for_changing(phnb_lst,last_name)
    if type(cont_ind)==str:
        print(cont_ind) 
    else:
        print_contact([phnb_lst[cont_ind]])
        delete=''
        while delete not in ['yes','no']:
            delete=input("Подтвердите удаление данного контакта - напечатайте yes или no: ")
        if delete=='yes':
            phnb_lst.pop(cont_ind)
            print("Данный контакт удален\n")

def find_by_number(phnb_lst, tel_number):
    not_find_contact=True
    for i in phnb_lst:
        if i['Телефон']==tel_number:
            print_contact([i]) 
            not_find_contact=False
    if not_find_contact:
        print("Контакта с таким номером телефона нет в справочнике")

def add_new_contact(phnb_lst):
    new_contact_data={}
    fields=['id','Фамилия', 'Имя', 'Телефон', 'Описание']
    letter_symbols=[chr(i) for i in range(1040,1104)]+[chr(i) for i in range(65,91)]+[chr(i) for i in range(97,123)] 
    new_contact_data['id']=give_id_to_new_contact(phnb_lst)
    for i in fields[1:]:
        new_contact_data[i]=input(f'Введите данные для поля "{i}": ').strip().replace(',','') 
    while set(new_contact_data['Фамилия'])&set(letter_symbols)==set():
        print("Поле 'Фамилия' обязательно для заполнения и должно содержать буквенные символы")
        new_contact_data['Фамилия']=input(f"Введите данные для поля 'Фамилия': ").strip().replace(',','')
    if new_contact_data['Телефон']!='' and new_contact_data['Телефон'] in [i['Телефон'] for i in phnb_lst]: 
        exist_number_ind=[i['Телефон'] for i in phnb_lst].index(new_contact_data['Телефон']) 
        print("Контакт с таким номером уже существует!")
        print_contact([phnb_lst[exist_number_ind]])
    else:
        phnb_lst.append(new_contact_data)
        print('Контакт добавлен в справочник')
        print_contact([new_contact_data])
    

def write_txt(filename , phnb_lst):
    with open(filename,'w',encoding='utf-8') as phout:
        for i in range(len(phnb_lst)):
            s='' 
            for v in phnb_lst[i].values():
                s+=v+','
            phout.write(f'{s[:-1]}\n')



def add_new_contact_from_another_phonebook(file_name,phonebook1): 
    try:
        phonebook2=read_txt(file_name)
    except FileNotFoundError:
        return 'С таким именем файла нет'  
    print_phonebook(phonebook2)
    id_for_copy=input("Введите id контакта, который Вы хотите скопировать (или напечатайте 'выйти'): ")
    if id_for_copy=='выйти':
        return ''
    if id_for_copy in [i['id'] for i in phonebook2]:
        id_contact_index=[i['id'] for i in phonebook2].index(id_for_copy)
        contact_for_copy=phonebook2[id_contact_index]
    else:
        return 'Контакта с таким id в данном справочнике нет'
    if contact_for_copy['Телефон']!='' and contact_for_copy['Телефон'] in [i['Телефон'] for i in phonebook1]:
        print('Внимание!')
        find_by_number(phonebook1, contact_for_copy['Телефон'])
        return 'Контакт с таким номером уже есть в справочнике, копирование не выполнено'
    else:
        contact_for_copy['id']=give_id_to_new_contact(phonebook1)
        return contact_for_copy


def work_with_phonebook(filename):
	

    choice=show_menu()

    phone_book=read_txt(filename) 



	

    choice=show_menu()

    phone_book=read_txt('phonebook.csv', 'r')

    while (choice!=7):

        if choice==1:
            print_result(phone_book)
        elif choice==2:
            last_name=input('lastname ')
            print(find_by_lastname(phone_book,last_name))
        elif choice==3:
            last_name=input('lastname ')
            new_number=input('new  number ')
            print(change_number(phone_book,last_name,new_number))
        elif choice==4:
            lastname=input('lastname ')
            print(delete_by_lastname(phone_book,lastname))
        elif choice==5:
            number=input('number ')
            print(find_by_number(phone_book,number))
        elif choice==6:
            user_data=input('new data ')
            add_user(phone_book,user_data)
            write_txt('phonebook.txt',phone_book)


        choice=show_menu()

work_with_phonebook('phonebook.txt')