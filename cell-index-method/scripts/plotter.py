import sys

import matplotlib.pyplot as plt


def get_first_word(s):
    words = s.split()
    if words:  # Check if the list is not empty
        return words[0]
    return ''  # Return an empty string if no words are found


def get_first_two_numbers(s):
    # Split the string into words
    words = s.split()

    # Ensure there are at least two words
    if len(words) < 2:
        raise ValueError("The input string does not contain at least two words.")

    # Extract the first two words
    first_word = float(words[0])
    second_word = float(words[1])

    # Return the words as a tuple
    return first_word, second_word


def create_dict_from_string(s):
    # Split the string into a list of words
    words = s.split()

    if not words:
        # Handle the case where the input string is empty
        return '', []

    # Extract the first word
    first_number = int(words[0])

    # Extract the rest of the words
    remaining_numbers = int(words[1:])

    # Create and return the dict
    return {first_number: remaining_numbers}


if __name__ == '__main__':
    inpt = sys.argv[1]
    with open(f"{sys.argv[2]}", "r") as f:
        lines1 = f.readlines()
        inputStaticNumbers = [float(get_first_word(line.strip())) for line in lines1[2:]]
    with open(f"{sys.argv[3]}", "r") as g:
        lines2 = g.readlines()
        inputDynamicNumbers = [get_first_two_numbers(line.strip()) for line in lines2[1:]]
    with open(f"{sys.argv[4]}", "r") as h:
        outputNumbers = {int(line.strip().split()[0]): line.strip().split()[1:] for line in h}

        # Extract horizontal and vertical positions
        x_coords, y_coords = zip(*inputDynamicNumbers)

        # Define the fixed radius for the circles
        radius = 0.5

        # Create a figure and axis for plotting
        fig, ax = plt.subplots()

        # Plot each coordinate as a circle
        for i, (x, y) in enumerate(inputDynamicNumbers):
            circle = plt.Circle((x, y), radius, color=f"{'red' if i == int(inpt) else 'blue' if str(i) in
                                outputNumbers.get(int(inpt), None) else 'black'}", fill=True)
            ax.add_artist(circle)

        # Set the limits of the plot
        ax.set_xlim(min(x_coords) - 1, max(x_coords) + 1)
        ax.set_ylim(min(y_coords) - 1, max(y_coords) + 1)

        # Set equal scaling
        ax.set_aspect('equal')

        # Add grid and labels
        ax.grid(True)
        ax.set_xlabel('Horizontal Position')
        ax.set_ylabel('Vertical Position')
        ax.set_title('2D Plot of Circles')

        # Show the plot
        plt.show()
