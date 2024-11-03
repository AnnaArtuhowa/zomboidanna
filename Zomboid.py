import csv

class FileReader:
    """
    Класс FileReader отвечает за чтение CSV-файлов и возврат данных
    в виде списка словарей, где каждый словарь представляет строку CSV-файла.
    """
    @staticmethod
    def read_csv(file_path):
        with open(file_path, newline='') as file:
            return list(csv.DictReader(file))


class ItemManager:
    """
    Класс ItemManager управляет данными предметов: загрузка, поиск по ID и имени.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.items = []

    def load_items(self):
        self.items = FileReader.read_csv(self.file_path)

    def get_items_by_id(self, item_id):
        return [item for item in self.items if item['ID'] == str(item_id)]

    def search_by_name(self, name):
        return [item for item in self.items if name.lower() in item['Name'].lower()]


class CSVSurvivorItems:
    """
    Класс для работы с предметами выживальщика из CSV-файла.
    """
    def __init__(self, file_path):
        self.item_manager = ItemManager(file_path)
        self.item_manager.load_items()

    def display_items(self, page_size=10, page_number=1, filter_by=None, filter_value=None):
        # Применение фильтрации, если заданы критерии
        items_to_display = (
            [item for item in self.item_manager.items if str(item.get(filter_by, "")).lower() == str(filter_value).lower()]
            if filter_by and filter_value
            else self.item_manager.items[(page_number - 1) * page_size : page_number * page_size]
        )

        if items_to_display:
            column_widths = {'ID': 5, 'Name': 20, 'Type': 15, 'Condition': 10, 'Amount': 7}
            header = f"{'ID'.ljust(column_widths['ID'])} | {'Name'.ljust(column_widths['Name'])} | {'Type'.ljust(column_widths['Type'])} | {'Condition'.ljust(column_widths['Condition'])} | {'Amount'.ljust(column_widths['Amount'])}"
            print(header)
            print('-' * len(header))

            for item in items_to_display:
                row = f"{item['ID'].ljust(column_widths['ID'])} | {item['Name'].ljust(column_widths['Name'])} | {item['Type'].ljust(column_widths['Type'])} | {item['Condition'].ljust(column_widths['Condition'])} | {item['Amount'].ljust(column_widths['Amount'])}"
                print(row)
        else:
            print("Нет предметов для отображения по заданным критериям.")


# Пример использования
file_path = 'items.csv'
csv_items = CSVSurvivorItems(file_path)

# Вывод предметов по ID
csv_items.display_items(filter_by='ID', filter_value='2')

# Вывод предметов по имени
csv_items.display_items(filter_by='Name', filter_value='Nails')

# Постраничный вывод предметов
csv_items.display_items(page_size=10, page_number=1)
