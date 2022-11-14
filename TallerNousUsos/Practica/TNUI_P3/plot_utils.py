import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt

def plot_1d(X, Y, fig):
    ax = fig.gca()
    line, = ax.plot(X, Y)
    ax.grid(True)

def plot_2d(X, Y, Z, fig, transparent=False):
    # Surface plot 3D + contour plot
    ax = fig.gca(projection='3d')
    if transparent:
        ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
    else:
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        
    ax.contour(X,Y,Z,30,zdir='z',offset=0)

def plot_gradient(X, Y, grad, fig):
    fig = fig
    ax = fig.gca()
    for x,y,g in zip(X, Y, grad):
        ax.arrow(x = x, y = y, dx = g, dy = 0, 
                  head_width = 0.3, head_length=0.4, fc='black', ec='black')
            
def plot_gradient_descend_1d(f, X, points, minimum, fig):
    plot_1d(X, f(X), fig)
    ax = fig.gca()
    ax.scatter(points, f(points), c='black')
    ax.plot(points, f(points), c='black')
    
def plot_gradient_descend_2d(f, grad, X, Y, points, minimum, fig):
    project_gradient(f, grad, fig, contour=30)
    ax = fig.gca()
    ax.scatter(points[:, 0], points[:, 1], c='black')
    ax.plot(points[:, 0], points[:, 1], c='black')
    
def generate_grid(function, axisX=[-2, 2, 0.05], axisY=[-2, 2, 0.05]):
    # Function to analyze
    X = np.arange(axisX[0], axisX[1], axisX[2])
    Y = np.arange(axisY[0], axisY[1], axisY[2])
    X, Y = np.meshgrid(X, Y)
    Z = function(*np.asarray([X, Y]))  
    return X, Y, Z

# Plot of the gradient
def project_gradient(f, grad_f, fig, contour=50):
    X, Y, Z = generate_grid(function = f)
    gradx, grady = grad_f(X,Y)
    ax = fig.gca()
    ax.contour(X, Y, Z, contour)
    ax.streamplot(X, Y, gradx, grady)

    
