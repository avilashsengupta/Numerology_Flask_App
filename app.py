from flask import Flask, render_template, request
app = Flask(__name__)

class Numerology:
    def __init__(self):
        self.grid_view = {4: 0, 9: 0, 2: 0, 3: 0, 5: 0, 7: 0, 8: 0, 1: 0, 6: 0}
        self.chaldean_num = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 8, 'g': 3, 'h': 5, 'i': 1,
                             'j': 1, 'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 7, 'p': 8, 'q': 1, 'r': 2,
                             's': 3, 't': 4, 'u': 6, 'v': 6, 'w': 6, 'x': 5, 'y': 1, 'z': 7}

    def reccursive_digitadd(self, numstr):
        ret = 0
        for i in str(numstr): ret = ret + int(i)
        if len(str(ret)) >= 2: ret = self.reccursive_digitadd(ret)
        return ret
    
    def life_path_number(self, dob):
        return self.reccursive_digitadd(dob.split('-')[-1])
    
    def destiny_path_number(self, dob):
        return self.reccursive_digitadd(dob.replace('-',''))
    
    def kua_number(self, dob, gender):
        x = self.reccursive_digitadd(dob.split('-')[0])
        if gender == 'male':
            x = self.reccursive_digitadd(11 - x)
            if x == 5: x = 2
        elif gender == 'female':
            x = self.reccursive_digitadd(4 + x)
            if x == 5: x = 8
        return x
    
    def maturity_number(self, name, dob):
        name_count = self.numerify_name(name)
        dest_numbr = self.destiny_path_number(dob)
        return self.reccursive_digitadd(name_count + dest_numbr)
    
    def numerify_name(self, name):
        name_quant = 0
        for i in str(name).lower():
            if i >= 'a' and i <= 'z': name_quant = name_quant + self.chaldean_num[i]
        name_quant = self.reccursive_digitadd(name_quant)
        return name_quant
    
    def obtain_combination(self, name, dob):
        name_quant = self.numerify_name(name)
        for i in self.grid_view.keys(): self.grid_view[i] = 0
        life_n = self.life_path_number(dob)
        dest_n = self.destiny_path_number(dob)

        for i in dob.replace('-',''):
            if i != '0': self.grid_view[int(i)] += 1
        self.grid_view[life_n] += 1
        self.grid_view[dest_n] += 1
        self.grid_view[name_quant] += 1
        return list(self.grid_view.values())

num = Numerology()
@app.route('/', methods = ['GET','POST'])
def homepage():
    ln_value = 0
    dn_value = 0
    kn_value = 0
    mn_value = 0

    occurance = list(num.grid_view.values())
    name_value = ''
    dob_value = ''
    gender_value = ''

    if request.method == 'POST':
        ln_value = num.life_path_number(request.form['dob'])
        dn_value = num.destiny_path_number(request.form['dob'])
        kn_value = num.kua_number(request.form['dob'], request.form['gender'])
        mn_value = num.maturity_number(request.form['name'], request.form['dob'])
        name_value = request.form['name']
        dob_value = request.form['dob']
        gender_value = request.form['gender']
        occurance = num.obtain_combination(request.form['name'], request.form['dob'])

    return render_template(
        template_name_or_list = 'main.html',
        grid_numbers = list(num.grid_view.keys()),
        num_occurs = occurance,
        life_number = ln_value,
        destiny_number = dn_value,
        kua_number = kn_value,
        maturity_number = mn_value,
        full_name = name_value,
        birthdate = dob_value,
        gender = gender_value.capitalize()
    )

if __name__ == '__main__': app.run(debug = True)