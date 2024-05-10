import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from moe_controller import MoeController


class Model(MoeController):
    def __init__(self):
        super().__init__(obstacle_interval=5, gate_reset_delay=20, print_state=False)

        print(
            """
                                                                                
 #***************#********#*#########%%#%%%%#%%%%%%%%@@%%%%%%%####**###***#%%%@ 
 =+==++++++#@@@@@@@@@@@%%%@@@%##+++++==+=+====+++++++++++*****#######%#%%#%##** 
 @@@@@@@@@@@@%-     % ====--=-*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#= 
#@        :         @ ++---:         :. ....@+                        #@@@@.@@@ 
                    @ .--        :=++=-==#. @                                 +@
 @@.                @##@    .====:..  -*#@  @                                   
 :#@@@@@@@@@@@     @  =+   +@*@@+   -=++=++ @@                                  
 =-:=.       =@@   @   -      *#@-  %#*=### #.                                  
         .  . .@@  -@@ *       .    ==:  .. @+                                  
    .:::---=+%@@      =@             .: .-.-                                    
#@@@@@@@@@@@@@@+                         .                                      
                      @             =*:                                         
                    @@@               ..   @-                                   
                  @@@@@        +*%#%%%=.  +@@@                                  
            @@@@@@@#+@@=           -     =@%@@@%:                               
      .  @@@@#- @@@=#*%@   .%           -@%+##@@  *+                            
    - @  :  :@@@  @@@#*@*     .       -:@@++###@@@    =@@@%@@@                  
   -          @*+  @@@%%@::.    #@@@@= -#+-+#%*-*@@+:=++.  @.                   
  +           @  +   @@@@*    .       =+:-+#%%=-*#@@@@                          
                 @     @@@#         :#=:-.+@@@@@@:     +    #                   
                =       @@@*       @@@@@@#@@       @@@@@@@@@#@@@@               
                         @@@@    %@@*+=*@@  @+    @@*=.#  -#   *@:              
                          @@@@  @@*=+=*@*           :      =@%@-.*@@@@-         
                           @%*.=%=---*@@    :%@@= ##@@@@@@@@+ #@%#=: .@@@@%     
                  :         @#=%%#**@@@   .    @@@@@@@@@@@@@@@@@:#@@@@@@@@@@@   
  @                    ::   @@:*=:+@@=      @@@=   :         @@#.-##*#@ @@@@@@@ 
  = @                        @@#%@@    :*@@@                    #@@@@@@    @@@@.
 *            + @          .  @**  -@@@@@#+*@@@@@@@@@@@@@@@@@@@@+:   :@@@@   := 
 -@                                 .----:::::::---:::--:----------=--=+#%@#+:. 
 %@%@@           .@*+- -@*#: -:  .==---=====++==+==+=======--------:::-:::.-::: 
 .:::*@@@@@@@@@@%%#*-    @@@@@@@@@%%***++***+++++*+++*+*++****+*+++++++++++===- 
                                                                                
                                                                                """
        )
