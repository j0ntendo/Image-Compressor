"""
NAME: 강우진 (Ujin Jonathan Kang)
YID: 

Data Structures
quadtree.py
"""

import numpy as np

class Node:
    """ Node class for quadtree
    
    1. Each node has four children:
    
        nw (northwest)
        ne (northeast)
        sw (southwest)
        se (southeast)

        Each children is the root of a subtree which
        covers the corresponding 'quadrant' of an image as below:

        |----|----|
        | nw | ne |
        |----|----|
        | sw | se |
        |----|----|
    
    2. Each node has a 'color' data.
    
    3. Each node covers a 'box' area of an image.
        The box has upperleft and downright corners with the
        following coordinates:
        
        (ul_x, ul_y): upperleft x and y
        (dr_x, dr_y): downright x and y
        
        (ul_x, ul_y)---------------|
              |                    |
              |                    |
              |                    |
              |                    |
              |                    |
              |---------------(dr_x, dr_y)
              
        Recall that the origin (0,0) is at the upperleft corner.
        
    4. Each node also stores its tree level.
    
    Note that you do not need a parent pointer to finish this assignment.
    Thus, a parent pointer is intentionally not included.
        
    """
    
    def __init__(self, color, corners, level):
        self.color = color
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None
        self.ul_x = corners[0]
        self.ul_y = corners[1]
        self.dr_x = corners[2]
        self.dr_y = corners[3]
        self.level = level
    
    
class Quadtree:
    """ Quadtree class
    
    Stores the image and its quadtree root.
    When initialized, only an emptry root exists.
    
    input:
        image: Image array
        root: The root of the quadtree which covers the entire image.
    """
    def __init__(self, image):
        self.image = image
        height, width = self.image.shape[0], self.image.shape[1]
        self.root = Node(None, [0, 0, width-1, height-1], 0)
        
        
def build_quadtree(qt):
    """ Build a quadtree
    
    Calls the recursive function to fully construct the quadtree
    of the given a Quadtree variable using its image.
    
    input:
        qt: Quadtree variable which has been initialized with
            an image and an empty root.
    """
    qt.root = build_quadtree_recursive(qt, qt.root)


def quadtree_to_image(qt, draw_box=False):
    """ Reconstruct the image array from quadtree
    Calls the recursive function to fully reconstruct the image
    array given a Quadtree variable qt.
    
    input:
        qt: Quadtree variable which is assumed to be constructed
            using build_quadtree (thus not empty).
        draw_box: If true, the image also draws a box for the area of each node.
            This makes it easier to see how the image is compressed.
            Default is False, so include the argument as True only when you want 
            the box to be drawn. So normally, just provide qt and node arguments.
            
    output:
        image: The reconstructed image array from the input qt.
            Note that this is *not* simply based on the leave colors.
            See its recursive call function for details.
    """
    qt.image = np.empty(qt.image.shape)  # reset the image
    quadtree_to_image_recursive(qt, qt.root, draw_box)
    image = np.squeeze(qt.image)
    return image

        
        
def compress_quadtree(qt, threshold):
    """ Compress quadtree colors
    
    Calls the recursive function to assign colors to the internal nodes
    based on the similarity of their childrens' colors.
    
    input:
        qt: Quadtree variable which is assumed to be constructed
            using build_quadtree (thus not empty).
        threshold: The value which decides if the colors are similar enough.
            See compress_quadtree_recursive.
            
    output:
        This does not return anything. Instead, directly modify
        the quadtree rooted at qt.root.
    """
    compress_quadtree_recursive(qt, qt.root, threshold)

        
def combine_colors(node, threshold):
    """ Combine the colors of the children nodes
    
    1. For 'node', first check if all children have colors. If at least
        one child has 'None' as color, then we cannot compress. Thus, skip.
        
    2. Otherwise, all four children have colors. Then, compute the similarity
        among the colors by taking the sum of the individual variance of the channels.
        If the sum of variance is less than threshold, then it implies the colors are
        "similar enough". Thus, return the average color.
        If the difference (sum of variance) is greater than or equal to threshold, then it implies the
        colors are not similar enough. Thus, we do not combine the colors and return None.
        
    input:
        node: The node which we compute the color for.
        threshold: The value which decides if the colors are similar enough.
            This is described above.
            
    output:
        Returns none if (1) not all four children have colors, 
            or (2) the colors are not similar enough.
        Returns the average color if (1) the colors are similar enough.
    """
    if node.nw.color is None or node.ne.color is None or node.sw.color is None or node.se.color is None:
        return None
    else:
        c1, c2, c3, c4 = node.nw.color, node.ne.color, node.sw.color, node.se.color
        difference = np.sum(np.var([c1, c2, c3, c4], axis=0))
        if difference < threshold:
            return np.mean([c1, c2, c3, c4], axis=0)
        else:
            return None
        

def draw_color(qt, node, draw_box):
    """ Draw the node.color within its area of qt.image
    
    Use this in quadtree_to_image_recursive.
    
    input:
        qt: Quadtree variable which is assumed to be constructed
            using build_quadtree (thus not empty).
        node: The current node which we fill the image area with.
        draw_box: If true, the image also draws a box for the area of each node.
            This makes it easier to see how the image is compressed.
            
    output:
        Does not return any output. Instead, directly modifies the
            image area based on the node's information.
    """
    qt.image[node.ul_y:node.dr_y+1, node.ul_x:node.dr_x+1] = node.color   
    if draw_box:
        qt.image[node.ul_y:node.dr_y+1, node.ul_x] = np.array([0, 0, 0])
        qt.image[node.ul_y, node.ul_x:node.dr_x+1] = np.array([0, 0, 0])
        
    
def compute_image_corners(node, child):
    """ Compute the image corners of the given child
    
    Give a node which covers an area of the image, compute the
    subareas (quadrants) which the given child has to cover.
    
    The quadrants exactly divide the parent's area into four
    equal squares.

        |----|----|
        | nw | ne |
        |----|----|
        | sw | se |
        |----|----|
        
    input:
        node: The parent node of the child we compute the corner for.
        child: The child node in string: {'nw', 'ne', 'sw', 'se'}
        
    output:
        Returns the child's corners in an array [ul_x, ul_y, dr_x, dr_y]
    """
    if child == 'nw':
        x_shift, y_shift = 0, 0
    elif child == 'ne':
        x_shift, y_shift = 1, 0
    elif child == 'sw':
        x_shift, y_shift = 0, 1
    elif child == 'se':
        x_shift, y_shift = 1, 1
    else:
        assert('Proper child needed.')
    
    half_width = (node.dr_x - node.ul_x + 1) / 2
    half_height = (node.dr_y - node.ul_y + 1) / 2 
    
    ul_x = int(node.ul_x + x_shift*half_width)
    ul_y = int(node.ul_y + y_shift*half_height)
    dr_x = int(ul_x + half_width - 1)
    dr_y = int(ul_y + half_height - 1)
    
    return [ul_x, ul_y, dr_x, dr_y]
    

    
def build_quadtree_recursive(qt, node):
    """ Recursively build a quadtree
    
    Given a Quadtree variable qt, recursively construct the
    full quadtree rooted at qt.root based on its image qt.image.
    
    The goal is to recursively make children where each child covers a
    quadrant (nw, ne, sw, or se) of the image.
    
    1. Check if the current node's area is just a single pixel. Our image
        has 256 width and 256 height, so eventually a single pixel has to be
        reached. (How do you check if the node's area is a single pixel?)
        
    2. If the current node's area is just a single pixel, the pixel value (color)
        should be assigned to the node's color. Also, this node becomes a leaf
        so do not recurse any further. You cannot recurse further anyway since
        a single pixel cannot be further divided into quadrants.
    
    3. Otherwise, a single pixel has not been reached yet. Thus, we can further
        divide the node's area into four quadrants. Create and assign a child node for
        each quadrant with correct quadrant corners using compute_image_corners.
    
    input:
        qt: Quadtree variable which has been initialized with
            an image and an empty root. Use this to access
            the image qt.image as you recurse.
        node: The current node to operate on.
        
    output:
        node: Return the modified node which should have its
            children assigned recursively.
    """

    # recursively call till it its one pixel
    if (node.dr_x - node.ul_x) == 0 and (node.dr_y - node.ul_y) == 0:
        # if single pixel then assign color and stop recursion
        node.color = qt.image[node.ul_y, node.ul_x]
        return node

    else:
        # create children
        node.nw = Node(None, compute_image_corners(node, 'nw'), node.level+1)
        build_quadtree_recursive(qt, node.nw)
        node.ne = Node(None, compute_image_corners(node, 'ne'), node.level+1)
        build_quadtree_recursive(qt, node.ne)
        node.sw = Node(None, compute_image_corners(node, 'sw'), node.level+1)
        build_quadtree_recursive(qt, node.sw)
        node.se = Node(None, compute_image_corners(node, 'se'), node.level+1)
        
        # recursively call for each child
        build_quadtree_recursive(qt, node.se)
        return node

    




def quadtree_to_image_recursive(qt, node, draw_box):
    """ Recursively reconstruct the image from quadtree
    
    Recursively traverses through the quadtree qt and modify the
    image (qt.image) as follows:
    
    1. The node may or may not have a color.
    
    2. If the node does have a color, it means the image area
        corresponding to this entire subtree is compressed down to that 
        single color.
        
        Thus, the corresponding area of the image (based on the box with 
        its corners ul_x, ul_y, dr_x, dr_y) should be filled with that color.
        
        Use the given function 
        
        **** draw_color(qt, node, draw_box) ****

        to assign the node's color to its area:
        
        (ul_x, ul_y)---------------|
              |                    |
              |                    |
              |        color       |
              |                    |
              |                    |
              |---------------(dr_x, dr_y)

              
        In this case, we do not wish to further check its children.
        
    3. If the node color is None, then we must check its children recursively.
    
    input:
        qt: Quadtree variable which is assumed to be constructed
            using build_quadtree (thus not empty).
        node: The current node to operatSe on.
        draw_box: If true, the image also draws a box for the area of each node.
            This makes it easier to see how the image is compressed.
            Default is False, so include the argument as True only when you want 
            the box to be drawn. So normally, just provide qt and node arguments.
            
    output:
        This does not return anything. Instead, directly modify
        qt.image so we avoid passing image as an input recursively.
    """
    # if node has color then fill the area with color
    while node.color is not None:
        draw_color(qt, node, draw_box)
        break
    if node.color is None:
        # recursively call for each child
        quadtree_to_image_recursive(qt, node.nw, draw_box)
        quadtree_to_image_recursive(qt, node.ne, draw_box)
        quadtree_to_image_recursive(qt, node.sw, draw_box)
        quadtree_to_image_recursive(qt, node.se, draw_box)
    

        

def compress_quadtree_recursive(qt, node, threshold):
    """ Compress quadtree colors
    
    If the colors of four children are similar enough,
    the average of the children's colors become the parent's color.
    Use combine_colors function. The logic is as follows:
    
    1. If the node is a leaf, then skip.
        
    2. Otherwise, we assume it has all four children. Recursively update
        their colors, then update the current node's color using combine_colors.
        
        **Note: If the node's color is not None (following if statement):
        
             if node.color is not None: <-- true
             
        We also prune (remove) the children by setting them to be None. We 
        do not need them since the childrens' colors and areas are not further considered.
        **Do not forget to do this: count_nodes can be used to count the number of
        nodes and check if the nodes are correctly removed or not.**
        
    Note that this function does not need a parent pointer.
    
    input:
        qt: Quadtree variable which is assumed to be constructed
            using build_quadtree (thus not empty).
        node: The current node to operate on.
        threshold: The value which decides if the colors are similar enough.
            If difference < threshold, then we decide that the childrens'
            colors are similar enough; thus the parent's color is assigned.
            Otherwise, the childrens' colors are not similar enough.
            
    output:
        This does not return anything. Instead, directly modify
        the quadtree rooted at qt.root.
    """
    #chk if leaf
    while node.nw is None and node.ne is None and node.sw is None and node.se is None:
        return None

    # recursively call for each child
    compress_quadtree_recursive(qt, node.nw, threshold)
    compress_quadtree_recursive(qt, node.ne, threshold)
    compress_quadtree_recursive(qt, node.sw, threshold)
    compress_quadtree_recursive(qt, node.se, threshold)

    # combine colors
    node.color = combine_colors(node, threshold)

    # prune children
    if node.color is not None:
        node.nw = None
        node.ne = None
        node.sw = None
        node.se = None
        


    

    
def count_nodes(node):
    """ Count the number of nodes in quadtree rooted at 'node'
    
    After compression, some nodes may be removed (pruned).
    Count the number of nodes in the current quadtree and return the value.
    If the given 'node' is qt.root, it counts all the nodes in the quadtree qt.
    Thus, this function technically returns the number of any subtree
    which has 'node' as its root.
    
    input:
        node: The root of the tree to count the number of nodes of.
        
    output:
        Return the number of nodes in qt rooted at node.
    """
    # recursively count nodes in quadtree
    if node is None: 
        return 0 # there is no node
    else:
        # return count of each child node + the current node
        return 1 + count_nodes(node.nw) + count_nodes(node.ne) + count_nodes(node.sw) + count_nodes(node.se)

    
def max_num_nodes(N):
    """ Compute the maximum number of nodes in a 
    quadtree from an array of size N by N
    
    In other words, this counts the number of nodes in a 
    full quadtree.
    Note: Do *NOT* simply use count_nodes function on a full quadtree.
    
    input:
        N: width (or height) of an array of size N by N
        
    output:
        num_nodes: the maximum number of nodes of a quadtree
            from an array of size N by N.
    """
    num_nodes = 0 #init

    if N == 1:
        num_nodes = 1
        return num_nodes
    else:
        num_nodes += N*N #count nodes
        return num_nodes + max_num_nodes(N/2) #recursively call the quadrants