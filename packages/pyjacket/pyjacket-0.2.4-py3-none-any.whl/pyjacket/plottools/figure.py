import plottools as plt
import numpy as np


# plt.set_style('test')
# plt.set_style('default')


# == Test Default plot
if False:
    x = [1, 2, 3]
    y = [4, 5, 6]

    fig, ax = plt.subplots(2, 2)
    
    plt.plot(x, y)
    plt.set_xlabel('x label [$um$]')
    plt.set_ylabel('y label [$u\phi$]')

    ax[0, 0].plot(x, y)
    ax[0, 0].set_xlabel('x label [$um$]')
    ax[0, 0].set_ylabel('y label [$u\phi$]')

    ax[0, 1].plot(x, y)
    ax[0, 1].set_xlabel('x label [$um$]')
    ax[0, 1].set_ylabel('y label [$u\phi$]')

    ax[1, 0].plot(x, y)
    ax[1, 0].set_xlabel('x label [$um$]')
    ax[1, 0].set_ylabel('y label [$u\phi$]')

    ax[1, 1].plot(x, y)
    ax[1, 1].set_xlabel('x label [$um$]')
    ax[1, 1].set_ylabel('y label [$u\phi$]')

    plt.show()
    
# == Test imshow == #
if False:
    img = np.random.randint(0, 255, (300, 300), dtype=np.uint8)
    fig, ax = plt.subplots(2, 2)
    plt.imshow(img)
    ax[0, 0].imshow(img)
    plt.show()
    
#  == Test histogram == #
if True:
    fig, ax = plt.subplots(2, 2)
    plt.hist(np.random.randint(0, 11, 500), bins=10)
    ax[0, 0].hist(np.random.randint(0, 11, 500), bins=10)
    plt.show()