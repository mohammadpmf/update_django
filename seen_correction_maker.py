with open('seen.txt', encoding='utf-8') as f, open('seen2.txt', 'w', encoding='utf-8') as f2:
    while True:
        t = f.readline().strip()
        index = t.find(':')
        if index != -1:
            number = t[:index]
            try:
                number=int(number)
                number+=3
                t = str(number)+t[index:]
            except:
                pass
        f2.write(f'{t}\n')
        if t=='':
            break