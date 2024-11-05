from math import exp, log, sqrt
from numba import njit
from options_models.utils import peizer_pratt_inverse

class LeisenReimer:
    """
    Class implementing the Leisen-Reimer binomial model for American options pricing
    and Greeks calculations.
    """

    @staticmethod
    @njit
    def price(sigma, S, K, T, r, q=0.0, option_type='calls', steps=100):
        """
        Calculate the price of an American option using the Leisen-Reimer binomial model.
        
        Parameters:
            sigma (float): Implied volatility.
            S (float): Current stock price.
            K (float): Strike price of the option.
            T (float): Time to expiration in years.
            r (float): Risk-free interest rate.
            q (float, optional): Continuous dividend yield. Defaults to 0.0.
            option_type (str, optional): 'calls' or 'puts'. Defaults to 'calls'.
            steps (int, optional): Number of steps in the binomial tree. Defaults to 100.
        
        Returns:
            float: The calculated option price.
        """
        return leisen_reimer_price_helper(sigma, S, K, T, r, q, option_type, steps)

    @staticmethod
    @njit
    def calculate_implied_volatility(
        option_price, S, K, T, r, q=0.0, option_type='calls', steps=100,
        max_iterations=100, tolerance=1e-8
    ):
        """
        Calculate the implied volatility for a given American option price using the Leisen-Reimer model.
        
        Parameters:
            option_price (float): Observed option price (mid-price).
            S (float): Current stock price.
            K (float): Strike price of the option.
            T (float): Time to expiration in years.
            r (float): Risk-free interest rate.
            q (float, optional): Continuous dividend yield. Defaults to 0.0.
            option_type (str, optional): 'calls' or 'puts'. Defaults to 'calls'.
            steps (int, optional): Number of steps in the binomial tree. Defaults to 100.
            max_iterations (int, optional): Maximum number of iterations for the bisection method. Defaults to 100.
            tolerance (float, optional): Convergence tolerance. Defaults to 1e-8.
        
        Returns:
            float: The implied volatility.
        """
        lower_vol = 1e-5
        upper_vol = 5.0

        for _ in range(max_iterations):
            mid_vol = (lower_vol + upper_vol) / 2
            price = leisen_reimer_price_helper(mid_vol, S, K, T, r, q, option_type, steps)

            if abs(price - option_price) < tolerance:
                return mid_vol

            if price > option_price:
                upper_vol = mid_vol
            else:
                lower_vol = mid_vol

            if upper_vol - lower_vol < tolerance:
                break

        return mid_vol

    @staticmethod
    @njit
    def calculate_delta(sigma, S, K, T, r, q=0.0, option_type='calls', steps=100):
        """
        Calculate the delta of an option using the Leisen-Reimer binomial model.
        
        Parameters:
            sigma (float): Implied volatility.
            S (float): Current stock price.
            K (float): Strike price.
            T (float): Time to expiration in years.
            r (float): Risk-free interest rate.
            q (float, optional): Continuous dividend yield. Defaults to 0.0.
            option_type (str, optional): 'calls' or 'puts'. Defaults to 'calls'.
            steps (int, optional): Number of steps in the binomial tree. Defaults to 100.
        
        Returns:
            float: The delta of the option.
        """
        dt = T / steps
        dx = sigma * sqrt(dt)
        u = exp(dx)
        d = exp(-dx)
        
        price_up = leisen_reimer_price_helper(sigma, S * u, K, T, r, q, option_type, steps)
        price_down = leisen_reimer_price_helper(sigma, S * d, K, T, r, q, option_type, steps)
        
        return (price_up - price_down) / (2 * S * (u - d))

    @staticmethod
    @njit
    def calculate_gamma(sigma, S, K, T, r, q=0.0, option_type='calls', steps=100):
        """
        Calculate the gamma of an option using the Leisen-Reimer binomial model.
        
        Parameters:
            sigma (float): Implied volatility.
            S (float): Current stock price.
            K (float): Strike price.
            T (float): Time to expiration in years.
            r (float): Risk-free interest rate.
            q (float, optional): Continuous dividend yield. Defaults to 0.0.
            option_type (str, optional): 'calls' or 'puts'. Defaults to 'calls'.
            steps (int, optional): Number of steps in the binomial tree. Defaults to 100.
        
        Returns:
            float: The gamma of the option.
        """
        d1 = (log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
        pdf_d1 = exp(-0.5 * d1**2) / sqrt(2 * 3.141592653589793)
        return exp(-q * T) * pdf_d1 / (S * sigma * sqrt(T))

    @staticmethod
    @njit
    def calculate_vega(sigma, S, K, T, r, q=0.0, option_type='calls', steps=100):
        """
        Calculate the vega of an option using the Leisen-Reimer binomial model.
        
        Parameters:
            sigma (float): Implied volatility.
            S (float): Current stock price.
            K (float): Strike price of the option.
            T (float): Time to expiration in years.
            r (float): Risk-free interest rate.
            q (float, optional): Continuous dividend yield. Defaults to 0.0.
            option_type (str, optional): 'calls' or 'puts'. Defaults to 'calls'.
            steps (int, optional): Number of steps in the binomial tree. Defaults to 100.
        
        Returns:
            float: The vega of the option.
        """
        epsilon = 1e-4
        price_up = leisen_reimer_price_helper(sigma + epsilon, S, K, T, r, q, option_type, steps)
        price_down = leisen_reimer_price_helper(sigma - epsilon, S, K, T, r, q, option_type, steps)

        return (price_up - price_down) / (2 * epsilon)

    @staticmethod
    @njit
    def calculate_theta(sigma, S, K, T, r, q=0.0, option_type='calls', steps=100):
        """
        Calculate the theta of an option using the Leisen-Reimer binomial model.
        
        Parameters:
            sigma (float): Implied volatility.
            S (float): Current stock price.
            K (float): Strike price of the option.
            T (float): Time to expiration in years.
            r (float): Risk-free interest rate.
            q (float, optional): Continuous dividend yield. Defaults to 0.0.
            option_type (str, optional): 'calls' or 'puts'. Defaults to 'calls'.
            steps (int, optional): Number of steps in the binomial tree. Defaults to 100.
        
        Returns:
            float: The theta of the option.
        """
        epsilon = 1e-5
        price = leisen_reimer_price_helper(sigma, S, K, T, r, q, option_type, steps)
        price_epsilon = leisen_reimer_price_helper(sigma, S, K, T - epsilon, r, q, option_type, steps)

        return (price_epsilon - price) / epsilon

    @staticmethod
    @njit
    def calculate_rho(sigma, S, K, T, r, q=0.0, option_type='calls', steps=100):
        """
        Calculate the rho of an option using the Leisen-Reimer binomial model.
        
        Parameters:
            sigma (float): Implied volatility.
            S (float): Current stock price.
            K (float): Strike price of the option.
            T (float): Time to expiration in years.
            r (float): Risk-free interest rate.
            q (float, optional): Continuous dividend yield. Defaults to 0.0.
            option_type (str, optional): 'calls' or 'puts'. Defaults to 'calls'.
            steps (int, optional): Number of steps in the binomial tree. Defaults to 100.
        
        Returns:
            float: The rho of the option.
        """
        epsilon = 1e-4
        price_up = leisen_reimer_price_helper(sigma, S, K, T, r + epsilon, q, option_type, steps)
        price_down = leisen_reimer_price_helper(sigma, S, K, T, r - epsilon, q, option_type, steps)

        return (price_up - price_down) / (2 * epsilon)

@njit
def leisen_reimer_price_helper(sigma, S, K, T, r, q=0.0, option_type='calls', steps=100):
    """
    Helper function to calculate the price of an American option using the Leisen-Reimer binomial model.
    
    Parameters:
        sigma (float): Implied volatility.
        S (float): Current stock price.
        K (float): Strike price of the option.
        T (float): Time to expiration in years.
        r (float): Risk-free interest rate.
        q (float, optional): Continuous dividend yield. Defaults to 0.0.
        option_type (str, optional): 'calls' or 'puts'. Defaults to 'calls'.
        steps (int, optional): Number of steps in the binomial tree. Defaults to 100.
    
    Returns:
        float: The calculated option price.
    """
    dt = T / steps
    discount = exp(-r * dt)
    u, d, p = leisen_reimer_ud_p(sigma, S, K, T, r, q, steps, option_type)

    prices = [S * (u ** (steps - j)) * (d ** j) for j in range(steps + 1)]
    values = [
        max(price - K, 0) if option_type == 'calls' else max(K - price, 0)
        for price in prices
    ]

    for i in range(steps - 1, -1, -1):
        for j in range(i + 1):
            values[j] = discount * (p * values[j] + (1 - p) * values[j + 1])
            price = S * (u ** (i - j)) * (d ** j)
            exercise_value = (
                max(price - K, 0) if option_type == 'calls' else max(K - price, 0)
            )
            values[j] = max(values[j], exercise_value)

    return values[0]

@njit
def leisen_reimer_ud_p(sigma, S, K, T, r, q, steps, option_type):
    """
    Calculate the up (u), down (d), and probability (p) factors for the Leisen-Reimer model.
    
    Parameters:
        sigma (float): Implied volatility.
        S (float): Current stock price.
        K (float): Strike price of the option.
        T (float): Time to expiration in years.
        r (float): Risk-free interest rate.
        q (float): Continuous dividend yield.
        steps (int): Number of steps in the binomial tree.
        option_type (str): 'calls' or 'puts'.

    Returns:
        Tuple[float, float, float]: (u, d, p) - up factor, down factor, and probability.
    """
    dt = T / steps
    dx = sigma * sqrt(dt)
    
    d1 = (log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)

    if option_type == 'calls':
        p = peizer_pratt_inverse(steps, d2)
    else:
        p = 1 - peizer_pratt_inverse(steps, -d2)
    
    u = exp(dx)
    d = exp(-dx)
    
    return u, d, p
