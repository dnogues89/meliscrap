class Visual:
    def __init__(self) -> None:
        self.all_models = ["Polo","Virtus","T-Cross","Nivus","Vento","Taos","Tiguan","Amarok"]
        self.list_of_models_to_scrap =[]

    def input_data_msg(self,msg):
        return input(msg)
    
    def error_opcion(self,fin):
        print(f'Opcion no valida, reingresar opcion entre 1 a {fin}')

    def menu(self):
        """
        This Method prints the menu in console
        returns the option tanken as an int
        
        """
        print("\n\n")
        print("#" * 20 + " MENU " + "#" * 20)
        print("1 - Scrap")
        print("2 - Completar Bases")
        print("3 - Consultas")
        print("9 - Finalizar")
        print("#" * 20 + " MENU " + "#" * 20)
        opcion = self.input_data_msg("Coloque la opcion deseada: ")
        print("\n\n")
        return int(opcion)

    def sub_menu_completar_bases(self):
        print("\n\n")
        print("#" * 11 + " COMPLETAR BASES " + "#" * 11)
        print("1 - Orden")
        print("2 - Dealers")
        opcion = self.input_data_msg("Coloque la opcion deseada: ")
        return int(opcion)
    
    def sub_menu_scrap(self):
        print("\n\n")
        print("#" * 20 + " SCRAP " + "#" * 20)
        print("1 - Todos los modelos")
        print("2 - Algunos modelos")
        opcion = self.input_data_msg("Coloque la opcion deseada: ")
        self.list_of_models_to_scrap = self.input_data_msg("Modelos a revisar (colocarlos con espacio) ").split()

    def sub_menu_consultas(self):
        pass