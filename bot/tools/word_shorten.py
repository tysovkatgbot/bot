def word_shorten(word):
    vowels = ['а', 'у', 'о', 'и', 'э', 'ы']
    consonants = ['б', 'в', 'г', 'д', 'ж', 'з', 'й', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'ф',
                  'х', 'ц', 'ч', 'ш', 'щ']
    count = 0
    for x in word:
        if x in consonants:
            count += 1
    if count >= 4:
        check = True
        for _ in word:
            if word[-1:] in vowels and check:
                word = word[:-1]
            else:
                check = False
    return word
