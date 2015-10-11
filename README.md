# knifty
KNIFTY Hebbian Neural Network

Gradient descent, the basis of most neural networks, is inefficient. I sought to make a neural network which learns in a way that is more similar to the way the human brain learns. Hebbian theory is a theory in neuroscience which proposes a mechanism by which the brain learns - by associating stimuli that occur frequently together. Colloquially, "Neurons that fire together, wire together," NFTWT, I designed Knifty around this principle. 

There are lots of implementations of Hebbian learning for neural networks out there, but I wanted to challenge myself to see if I could do it without using floats or division. I don't claim this is super original, just was something I want to try to get to work. 

Apologies for the lack of comments right now! 
To run, merely run the group_generator.py . The network will actualize on generated clustering data in n dimensions,
where n is specified by indim. 
