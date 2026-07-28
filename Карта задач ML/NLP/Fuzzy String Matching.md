Расстояние Левенштейна - считает, сколько минимальных изменений (замен букв, удалений, добавлений) нужно сделать, чтобы превратить одну строку в другую.

Врачи часто сокращают слова (например: _«Острый обструкт. бронхит»_ или _«Искривление нос. перегородки»_). Чтобы поймать такие случаи, используют **алгоритмы нечеткого сравнения строк (Fuzzy String Matching)**.

Библиотека в Python (например, `thefuzz` или `RapidFuzz`) умеет сравнивать фразы по схожести букв и выдавать процент совпадения от 0 до 100%.

- Вы настраиваете код: если фраза из текста врача похожа на диагноз из справочника **более чем на 80%**, мы считаем, что это он, и ставим `1`.


```
def extract_diagnoses(text, dictionary, threshold=70):
	found_diagnoses = [] 
	text_lower = text.lower() 
	
	for diag in dictionary: 
		diag_lower = diag.lower() 
		score = fuzz.partial_ratio(diag_lower, text_lower) 
		if score >= threshold: 
			found_diagnoses.append(diag) 
			
	return found_diagnoses
```
