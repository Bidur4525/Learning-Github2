{
	"cells": [
		{
			"cell_type": "code",
			"execution_count": 1,
			"metadata": {},
			"outputs": [],
			"source": [
				"import time\n",
				"import matplotlib.pyplot as plt\n",
				"from simple_pid import PID"
			]
		},
		{
			"cell_type": "code",
			"execution_count": 2,
			"metadata": {},
			"outputs": [],
			"source": [
				"class WaterBoiler:\n",
				"    \"\"\"\n",
				"    Simple simulation of a water boiler which can heat up water\n",
				"    and where the heat dissipates slowly over time\n",
				"    \"\"\"\n",
				"\n",
				"    def __init__(self):\n",
				"        self.water_temp = 20\n",
				"\n",
				"    def update(self, boiler_power, dt):\n",
				"        if boiler_power > 0:\n",
				"            # Boiler can only produce heat, not cold\n",
				"            self.water_temp += 1 * boiler_power * dt      #### increasing heat temperature equation\n",
				"\n",
				"        # Some heat dissipation\n",
				"        self.water_temp -= 0.02 * dt\n",
				"        return self.water_temp"
			]
		},
		{
			"cell_type": "code",
			"execution_count": 3,
			"metadata": {},
			"outputs": [],
			"source": [
				"if __name__ == '__main__':\n",
				"    boiler = WaterBoiler()\n",
				"    water_temp = boiler.water_temp\n",
				"\n",
				"    pid = PID(5, 0.01, 0.1, setpoint=water_temp)\n",
				"    pid.output_limits = (0, 100)\n",
				"\n",
				"    start_time = time.time()\n",
				"    last_time = start_time\n",
				"\n",
				"    # Keep track of values for plotting\n",
				"    setpoint, y, x = [], [], []\n",
				"\n",
				"    while time.time() - start_time < 10:\n",
				"        current_time = time.time()\n",
				"        dt = current_time - last_time\n",
				"\n",
				"        power = pid(water_temp)\n",
				"        water_temp = boiler.update(power, dt)\n",
				"\n",
				"        x += [current_time - start_time]\n",
				"        y += [water_temp]\n",
				"        setpoint += [pid.setpoint]\n",
				"\n",
				"        if current_time - start_time > 1:\n",
				"            pid.setpoint = 100\n",
				"\n",
				"        last_time = current_time"
			]
		},
		{
			"cell_type": "code",
			"execution_count": 4,
			"metadata": {},
			"outputs": [
				{
					"data": {
						"image/png": "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c9m5cyeRSIR169bxne98B0h0pd29ezcTJkzgS1/6Eps3b6awsJB33nkHgNmzZ3PTTTfR1tbGNddcw8yZM09aw6JFiygsLKSxsZHf//73LFp07MRJa2srAL/73e9Ys2YNANdffz133pmaYV0KhZBEGoLZUTVGQSSrDB48uPN+QUFB53ZBQQGxWIzCwkLWrFnDWWed9ZHX3X333ZSXl/Pqq68Sj8cpKSkB4NJLL+X555/nmWee4frrr+drX/saN9xww0euJR4/lmDYsGEAxONxRo0axebNm7utNR3XIzX3UUi0joJIbrryyiu57777cHcANm3aBMDBgwcZP348BQUF/OQnP6G9vR2AXbt2UVZWxs0338ySJUt45ZVXACgvL2fr1q3E43GefPLJbo81cuRIJk+ezOOPPw4kTju/+uqrAFx88cX87Gc/A2DVqlUp+3wKhZAcCwW1FERyyV133UVbWxvnnXce06dP56677gLg1ltvpbq6mjlz5vDOO+90ftt/7rnnmDlzJueffz5r1qzhjjvuAGDFihVcffXVzJ07l/Hjx/d4vFWrVvHQQw8xY8YMpk2bxtq1iY6Z9957L/fffz+zZ8/m4MGDKft81pF2uaiqqspramrCLqN3Hr4KCgr51th/5rE/vs8b37pSXVJFgK1bt3LOOeeEXUbe6e7P1cw2untVd89XSyEktRqjICJZSKEQksQ6CrqeICLZRaEQEg1cE5FspFAIQSzuHGrRGAURyT4KhRC0xuIATByl00cikl0UCiHoCAW1FEQk2ygUQtDalhjUolAQyR4NDQ088MADaT/OU089xZtvvpn24/SVQiEELbE4Q4oLGTNsUNiliEigt6Hg7sTj8V4fJ9tDQXMfhaC1rV1jFERO5L+WwYevp/Y9P3YuXLWix4eXLVvG9u3bmTlzJpdddhmvvfYa0WiUtrY27rnnns7psa+66iouu+wyXnzxRZ566il+/OMfs2rVKiZNmsS4ceO44IIL+OpXv8r27dv/ZMrrAwcOsG7dOn77299yzz33sGbNGs4444zUfs5+UiiEoDUWp6Jcp45EssmKFSt444032Lx5M7FYjKamJkaOHMm+ffuYM2cOCxYsAODtt9/mhz/8IQ888AA1NTWsWbOGTZs2EYvFmDVrFhdccAEAS5cu7XbK6wULFnD11Vfz2c9+NsyP2yOFQghaY+26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",
						"text/plain": [
							"<Figure size 432x288 with 1 Axes>"
						]
					},
					"metadata": {
						"needs_background": "light"
					},
					"output_type": "display_data"
				}
			],
			"source": [
				"    plt.plot(x, y, label='measured')\n",
				"    plt.plot(x, setpoint, label='target')\n",
				"    plt.xlabel('time')\n",
				"    plt.ylabel('temperature')\n",
				"    plt.legend()\n",
				"    plt.show()"
			]
		},
		{
			"cell_type": "code",
			"execution_count": null,
			"metadata": {},
			"outputs": [],
			"source": [
				"import numpy as np\n",
				"import matplotlib as plt"
			]
		},
		{
			"cell_type": "code",
			"execution_count": 7,
			"metadata": {},
			"outputs": [
				{
					"name": "stdout",
					"output_type": "stream",
					"text": [
						"Area of Rectangle: 19200 cm^2\n"
					]
				}
			],
			"source": [
				"class Rectangle:\n",
				"    def __init__(self, length, breadth, unitcost=0):\n",
				"        self.length=length\n",
				"        self.breadth=breadth\n",
				"        self.unit_cost=unitcost\n",
				"\n",
				"    def get_perimeter(self):\n",
				"        return 2*(self.length+self.breadth)\n",
				"\n",
				"    def get_area(self):\n",
				"        return self.length*self.breadth\n",
				"\n",
				"\n",
				"a=Rectangle(160, 120, 2000)\n",
				"print(\"Area of Rectangle: %s cm^2\" %(a.get_area()))\n"
			]
		},
		{
			"cell_type": "code",
			"execution_count": 28,
			"metadata": {},
			"outputs": [
				{
					"name": "stdout",
					"output_type": "stream",
					"text": [
						"Seconds since epoch = 1655170416.3056161\n"
					]
				}
			],
			"source": [
				"import time\n",
				"seconds = time.time()\n",
				"print(\"Seconds since epoch =\", seconds)"
			]
		},
		{
			"cell_type": "code",
			"execution_count": null,
			"metadata": {},
			"outputs": [],
			"source": [
				"import numpy as np\n",
				"import time\n",
				"import matplotlib.pyplot as plt\n",
				"from simple_pid import PID\n",
				"\n",
				"class KalmanFilter(object):\n",
				"    def __init__(self,dt,u,std_acc,std_meas):\n",
				"        self.dt = dt\n",
				"        self.u = u\n",
				"        self.std_acc = std_acc\n",
				"        self.A = np.matrix([[1, self.dt],\n",
				"                            [0, 1]])\n",
				"        self.B = np.matrix([[(self.dt**2)/2], [self.dt]]) \n",
				"        self.H = np.matrix([[1,0]])\n",
				"        self.Q = np.matrix([[(self.dt**4)/4, (self.dt**3)/2],\n",
				"                            [(self.dt**3)/2, self.dt**2]]) * self.std_acc**2\n",
				"        self.R = std_meas**2\n",
				"        self.P = np.eye(self.A.shape[1])\n",
				"        self.x = np.matrix([[0],[0]])\n",
				"\n"
			]
		}
	],
	"folders": [],
	"metadata": {
		"interpreter": {
			"hash": "ad2bdc8ecc057115af97d19610ffacc2b4e99fae6737bb82f5d7fb13d2f2c186"
		},
		"kernelspec": {
			"display_name": "Python 3.9.7 ('base')",
			"language": "python",
			"name": "python3"
		},
		"language_info": {
			"codemirror_mode": {
				"name": "ipython",
				"version": 3
			},
			"file_extension": ".py",
			"mimetype": "text/x-python",
			"name": "python",
			"nbconvert_exporter": "python",
			"pygments_lexer": "ipython3",
			"version": "3.9.7"
		},
		"orig_nbformat": 4
	},
	"nbformat": 4,
	"nbformat_minor": 2
}
