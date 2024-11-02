
from textual.app import App, ComposeResult
from textual.widgets import Static, Input, Header,Footer
from textual.screen import ModalScreen
from .confmscn import Confirm_Screen
from textual import on, work
import pandas as pd
from .paxModule import *
from .serialNoValidator import SerialNoValidator
from .paxStoreChecker import PaxStoreChecker, NA_Handler
from .functionsScreen import FunctionsScreen
from .replace_terminal_screen import ReplaceTerminal

class Scan_serials(ModalScreen):

    """SERIAL NUMBER INPUT"""
    BINDINGS = [("escape", "app.pop_screen", "BACK"),("0000", "", "SUBMIT"),("BKSPC", "", "Del item")]


    def __init__(self):
        self.order_of_input = [] # list of all input in order of input
        self.serialNoList = [] # list of serialnumbers in paxstore
        self.copySerialNoList = self.serialNoList
        self.detailsList = []
        self.serialValidator = SerialNoValidator()  # Create an instance of the validator
        self.exceptions = []
         # list of all terminals not found in PaxStore
        self.ops = apiPaxFunctions()
        super().__init__()
    
    def compose(self) -> ComposeResult:
        
        yield Header(name='PaxTools')
        yield Static("SCAN OR TYPE SERIAL NUMBER:")
        yield Input(placeholder="S/N",validators=[self.serialValidator])
        yield Footer()
    
    @on(Input.Submitted)
    @work
    async def update_serial_list(self):
        user_input = self.query_one(Input)
        self.order_of_input.append(user_input.value) # add all input to order of input list
        serialNo = user_input.value
        self.mount(Static(str(user_input.value)))
        if user_input.value == "BKSPC":
            self.serialNoList.pop()
            self.serialNoList.pop()
        if ":" in user_input.value:
            self.serialNoList.pop()
            self.app.bell()
        if user_input.value == "0000":
            self.disabled = True
            self.app.bell()
            self.order_of_input.pop()
            check = PaxStoreChecker(self.order_of_input)

            if check.not_in_paxStore:
                if await self.app.push_screen_wait(Confirm_Screen(f"These Terminals are not registered: {check.not_in_paxStore}\nDo you want to register now? ")):
                    adder = NA_Handler(check.not_in_paxStore)
                    if adder.exceptions_list:
                        self.exceptions.extend(exception for exception in adder.exceptions_list)
                        if await self.app.push_screen_wait(Confirm_Screen(f"The following can not be added to the PaxStore\n{adder.exceptions_list}\n Please escalate to Eval 2. Please choose:", "Remove", "Replace")):
                            for exception in self.exceptions:
                                replace = await self.app.push_screen_wait(ReplaceTerminal(exception))
                                index = self.order_of_input.index(exception)
                                self.order_of_input[index] = replace
                                self.app.notify(str(f'{exception} replaced with {replace}'))
                        else:
                            if await self.app.push_screen_wait(Confirm_Screen(f"Please remove these terminals before continuing \n{check.not_in_paxStore}")):
                                pass
                            self.order_of_input = [serial for serial in self.order_of_input if serial not in self.exceptions]
                    self.app.notify(str(adder.terminal_data))

                else: 
                    if await self.app.push_screen_wait(Confirm_Screen(f"Please remove these terminals before continuing \n{check.not_in_paxStore}")):
                        pass
                    self.exceptions.extend(serial for serial in check.not_in_paxStore)
            final_list = [serial for serial in self.order_of_input if serial not in self.exceptions]
            if await self.app.push_screen_wait(Confirm_Screen("Please connect to network and open PaxStore on terminals")):
                self.group = await self.ops.startPaxGroup(final_list, handleAccessory=False)
                self.app.push_screen(FunctionsScreen(pd.DataFrame(self.group)))      
        user_input.clear()



        
class scan_v2(App):

    def on_mount(self) -> None:
         self.push_screen(Scan_serials())
         

if __name__ == "__main__":
    app = scan_v2()
    app.run()


        

        
