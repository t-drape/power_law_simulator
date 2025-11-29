# power_law_simulator
A simulator in Python to visualize criticality and the power law. Applications are Wildfires, Earthquakes, Disease, and Curie Temperatures for Magnets. Idea from Veritasium video.

The higher the weight, the lower the probability that a coin flip will return True. 

The dimensions of the window are 800x800 pixels. Green tiles represent trees, red tiles represent fires, and black tiles represent open land. Each tile is 40x40 pixels, and the board is 20x20. If the board is too large, then I encountered a maximum recursion error. Python only allows recursion up to 1,000 calls. However, if each cell of the board catches fire, the calls to the lightning function would exceed 1,000. Thus, I reduced the size to resolve this issue.
