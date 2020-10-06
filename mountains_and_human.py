HUMAN_HEIGHT = 3
HUMAN_WIDTH = 3
HUMAN_LEG_OFFSET = 1


def print_2d_array(arr):
    """Print the 2D Array"""
    print(f"Height = {len(arr)}, Width = {len(arr[0])}")
    for row in arr:
        for item in row:
            print(f"{item}", end="")
        print()


def increasing_slope(index):
    """Returns if the slope is increasing which is the even number"""
    return index % 2 == 0


def get_indicator(index):
    """Returns the indicator for increasing or decreasing slope"""
    return "/" if increasing_slope(index) else "\\"


def add_human_at(new_arr, human_location, height):
    """Adds Human to the Array"""
    human_x = human_location[0]
    human_y = human_location[1]
    # Hardcoded points based on Center Bottom
    new_arr[height - human_y - 1][human_x - 1] = " "
    new_arr[height - human_y - 1][human_x] = "○"
    new_arr[height - human_y - 1][human_x + 1] = " "
    new_arr[height - human_y][human_x - 1] = "/"
    new_arr[height - human_y][human_x] = "|"
    new_arr[height - human_y][human_x + 1] = "\\"
    new_arr[height - human_y + 1][human_x - 1] = "<"
    new_arr[height - human_y + 1][human_x] = " "
    new_arr[height - human_y + 1][human_x + 1] = ">"


def create_line(y0, x0, y1, x1, index):
    """Generator that Returns the diagonal line from x,y to x1,y1"""
    # Return the first point
    yield y0, x0
    # Loop until we reach the last point
    while y0 != y1 and x0 != x1:
        # increase or decrease y according to the slope
        y0 = y0 + (-1 if increasing_slope(index) else 1)
        x0 += 1
        # Return in between points. This is also the last point
        yield y0, x0


def get_2d_mountains_from_1d_sum(arr, height, width, human_location):
    # Generate the X,Y Plane
    new_arr = []
    for i in range(height + HUMAN_HEIGHT):
        mountain_row = []
        for j in range(width + HUMAN_LEG_OFFSET):
            mountain_row.append(" ")
        new_arr.append(mountain_row)

    # Offset to maintain the ground at the bottom
    ground = height + HUMAN_HEIGHT
    # Prev x and y to keep track of the last location
    prev_x, prev_y = 0, 0
    for index, [x, y] in enumerate(arr):
        # Get the indicator for the current slope;i.e even for increment and odd for decrement
        indicator = get_indicator(index)

        # Calculations are all based from below the list hence (ground - <value>)
        #
        # Print the Mountains After Human (+1 Index due to human leg space)
        if prev_x >= human_location[0]:
            start_x, start_y = ground - prev_y - 1, prev_x + HUMAN_LEG_OFFSET
            end_x, end_y = ground - y - 1, x - 1 + HUMAN_LEG_OFFSET
        # Print the Mountains Before Human
        else:
            start_x, start_y = ground - prev_y - 1, prev_x
            end_x, end_y = ground - y - 1, x - 1

        # Iterate between the points to print indicator
        for (point_y, point_x) in create_line(start_x, start_y, end_x, end_y, index):
            new_arr[point_y][point_x] = indicator

        # Maintain Previous to maintain start of the next line
        prev_y = y
        prev_x = x

    # Add Human to the list
    add_human_at(new_arr, human_location, height)
    # Print the List
    print_2d_array(new_arr)


def generate_mountains(nums):
    # Create a Prefix list of all inputs with respect to slope
    sum_nums = []
    sum_at_position = 0
    previous_sum = 0
    total_width = 0
    max_height = 0
    human_location = []
    for index, item in enumerate(nums):
        # + or - numbers to get prefix list
        if index % 2 == 0:
            sum_at_position += (item - 1)
        else:
            sum_at_position -= (item - 1)

        # Calculate width by the difference in last and current position
        # eg: 3 2 -> it needs to move x by 1
        total_width += abs(sum_at_position - previous_sum) + 1

        # Check and maintain the max_height for humans location
        if sum_at_position > max_height:
            max_height = sum_at_position
            human_location = [total_width, max_height]

        previous_sum = sum_at_position
        sum_nums.append([total_width, sum_at_position])

    get_2d_mountains_from_1d_sum(sum_nums, max_height + 1, total_width, human_location)


def print_mountains_human_from_input(nums):
    generate_mountains(nums)


print_mountains_human_from_input(
    [3, 1, 2, 3, 6, 2, 3, 6, 2, 3, 6, 3, 2, 3, 6, 2, 3, 4, 3, 2, 5, 4, 2, 1, 2, 1, 2, 3, 1, 2, 6, 2, 3, 6, 2, 3, 6,
     3,
     2, 3, 1, 5, 3, 2, 1, 2, 4, 2, 1, 8, 1, 2])
