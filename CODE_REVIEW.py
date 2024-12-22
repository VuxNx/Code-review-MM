import numpy as np
import gymnasium as gym
from gymnasium import spaces

# THIS IS CODE REVIEW FOR HARMONY 

"""
1. Follow the SPEC, stock has 3 type:
    a. -2: this postion is not avaliabel
    b. -1: this postion is empty
    c. 0 or greater: this postion is occupied
"""


def _get_info(self):
        """
        > This line code filled_ratio is to calculate the filled ratio of the stocks with mean through
        attribute cutted_stocks.
        
        > Futher information about attribute cutted_stocks:
            - cutted_stocks: list of integers 0 or 1, represent for the state of stock, is used or not.
        
        > Example: self.cutted_stocks = [0, 0, 1] => filled_ratio = 1/3 = 0.33
        """
        filled_ratio = np.mean(self.cutted_stocks).item()
        
        # trim_loss is used to store all trim_loss of each stock
        trim_loss = []

        """
        > Futher inforamtion about sid:
            -sid: index of stock in the list of stocks
            -self.cutted_stocks[sid]: check if the stock is used or not. If not, keep going to next stock.
        > Futher information about trim_loss:
            - trim_loss: list of float, represent for the trim loss of each stock.
            - trim_loss = (stock == -1).sum() / (stock != -2).sum(). This code means that: count all unit that equal to -1,
            meaning that this unit is empty, then divide by the number of unit that not equal to -2, meaning that this unit is used,
            include the empty unit.
        
        > After all, calculate the mean of trim_loss to get the final result.
        
        > Example: stock = np.array([
                                    [-1, -1,  1,  1],
                                    [ 1, -2,  1, -1],
                                    [-1,  1,  1, -2]
                                    ])
                => (stock == -1).sum() = 4, (stock != -2).sum() = 10 => trim_loss = 4/10 = 0.4
        """

        for sid, stock in enumerate(self._stocks):
            if self.cutted_stocks[sid] == 0:
                continue
            tl = (stock == -1).sum() / (stock != -2).sum()
            trim_loss.append(tl)
            
        # Check if trim_loss is true or not, if not, return 1 (absolute watse)
        trim_loss = np.mean(trim_loss).item() if trim_loss else 1

        return {"filled_ratio": filled_ratio, "trim_loss": trim_loss}
    


def step(self, action):
        """
        > Futher information about action:
            - action: dictionary, contain 3 keys: stock_idx, size, position
            - Remember that this arguments linked to get_action() function in Policy. This attribute is the action that called
            from get_action() function.
        """
        stock_idx = action["stock_idx"]
        size = action["size"]
        position = action["position"]

        width, height = size
        x, y = position

        # Check if the product is in the product list
        product_idx = None
        """
        > This loop is to validate that the product in action is in self._products or not. If yes, then check if the quantity of it,
        if it equal to 0, then continue to next product. If not, then assign the product index to product_idx.
        
        > size[::-1] is used to reverse the size of product. This is because the product can be rotated.
        """
        for i, product in enumerate(self._products):
            if np.array_equal(product["size"], size) or np.array_equal(
                product["size"], size[::-1]
            ):
                if product["quantity"] == 0:
                    continue

                product_idx = i  # Product index starts from 0
                break
    

        if product_idx is not None:
            # Check if the stock is in the stock list through index.
            if 0 <= stock_idx < self.num_stocks:
                stock = self._stocks[stock_idx]
                # Check if the product fits in the stock
                
                
                """
                > np.any(stock != -2, axis=1): create a boolean array, if the element in stock is not equal to -2, then return True, else False.
                Then the np.any(..., axis=1) is to check if there is any True in the row. If yes, then return True, else False.
                
                > Example: stock = np.array([
                                [-2, -2, -1, -1, -1],
                                [-2, -2, -1, -1, -1],
                                [-2, -2, -2, -1, -1],
                                [-2, -2, -2, -2, -2],
                            ])
                            
                    -then, stock != -2, will make this stock looks like:
                            stock_temp = array([
                                [False, False,  True,  True,  True],
                                [False, False,  True,  True,  True],
                                [False, False, False,  True,  True],
                                [False, False, False, False, False],
                            ])
                    -apply np(..., axis=1), it counts each rows and counts if this row contains at least one value != -2,
                    assign True to this row:
                            array([ True,  True,  True, False])
                    -sum to count the number of True.    
                """
                stock_width = np.sum(np.any(stock != -2, axis=1))
                stock_height = np.sum(np.any(stock != -2, axis=0))
                
                
                
                """
                > Check if this postion is valid or not when put one product at (x, y)
                """
                if (
                    x >= 0
                    and y >= 0
                    and x + width <= stock_width
                    and y + height <= stock_height
                ):
                    # Check if the position is empty
                    if np.all(stock[x : x + width, y : y + height] == -1):
                        self.cutted_stocks[stock_idx] = 1
                        stock[x : x + width, y : y + height] = product_idx
                        self._products[product_idx]["quantity"] -= 1


        # An episode is done iff the all product quantities are 0
        terminated = all([product["quantity"] == 0 for product in self._products])
        reward = 1 if terminated else 0  # Binary sparse rewards

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info
    


"""
> This function calcualte and create the action that agent wants to do bases on observation(current state) and info (likes futher information).

> Output of this function is action in step():
    -Example: {"stock_idx": 0, "size": [2, 3], "position": (0, 0)}    
"""
def get_action(observation, info):
    pass


def _can_place_(self, stock, position, prod_size):
        pos_x, pos_y = position
        prod_w, prod_h = prod_size
        """
        > This line code similar to the code in step(). Check the zone at (pos_x, pos_y) is all -1 (meanings that is available).
        """
        return np.all(stock[pos_x : pos_x + prod_w, pos_y : pos_y + prod_h] == -1)



if __name__ == "__main__":
    #This is temp env
    env = None
    observation, info = env.reset(seed=42)
         
    policy2210xxx = None
    
    for _ in range(200):
        """
        > Create action based on current state and info.
        """
        action = policy2210xxx.get_action(observation, info)
        
        observation, reward, terminated, truncated, info = env.step(action)
        print(info)