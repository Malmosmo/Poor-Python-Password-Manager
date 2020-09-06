class Database:
    def __init__(self):
        self.tables = {}

    def add_table(self, name, *args):
        if name not in self.tables:
            self.tables[name] = Table(name, *args)

        else:
            print("table already exists")        

    def add(self, table, **kwargs):
        if table in self.tables:
            self.tables[table].add(**kwargs)

        else:
            print("no table")

    def delete_table(self, name):
        del self.tables[name]

    def delete_entry(self, name, index):
        del self.tables[name].entries[index]

    def out(self):
        for name in self.tables.keys():
            print(name)
            self.tables[name].out()

class Table:
    def __init__(self, name, *args):
        self.name = name

        self.keys = args

        self.entries = {}

    def add(self, **kwargs):
        count = 0

        while True:
            if count not in self.entries:
                self.entries[count] = dict((key, kwargs[key]) for key in self.keys)
                break
            
            count += 1

    def out(self):
        for key, value in self.entries.items():
            print('     ', key, value)

if __name__ == "__main__":
    data = Database()

    data.add_table('General', 'password', 'url')

    data.add('General', password='test', url='buhhh')
    data.add('General', password='test', url='buhhh')

    data.out()

    data.delete_entry('General', 0)
    
    data.out()

    # data.delete_table('General')
    data.add('General', password='test', url='buhhh')

    data.out()