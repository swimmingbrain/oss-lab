import matplotlib.pyplot as plt

def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'): # If 'line' is not a header
                data.append([int(word) for word in line.split(',')])
    return data

if __name__ == '__main__':
    # Load score data
    class_kr = read_data('data/class_score_kr.csv')
    class_en = read_data('data/class_score_en.csv')
    
    # Prepare midterm, final, and total scores
    midterm_kr, final_kr = zip(*class_kr)
    total_kr = [40/125*midterm + 60/100*final for (midterm, final) in class_kr]
    
    midterm_en, final_en = zip(*class_en)
    total_en = [40/125*midterm + 60/100*final for (midterm, final) in class_en]
    
    # Create 2 subplots in the same plot
    fig, (sp1, sp2) = plt.subplots(1, 2, figsize=(14, 6))

    # Plot midterm/final scores as points (first subplot)
    sp1.scatter(midterm_en, final_en, color='blue', label='English Class', alpha=0.7)
    sp1.scatter(midterm_kr, final_kr, color='red', label='Korean Class', alpha=0.7)
    sp1.set_xlim(0, 125)
    sp1.set_ylim(0, 100)
    sp1.set_xlabel('Midterm Scores')
    sp1.set_ylabel('Final Scores')
    sp1.set_title('Midterm/Final Scores')
    sp1.legend()
    sp1.grid(True)

    # Plot total scores as a histogram (second subplot)
    sp2.hist(total_en, bins=range(0, 105, 5), color='blue', alpha=0.7, label='English Class', edgecolor='black')
    sp2.hist(total_kr, bins=range(0, 105, 5), color='red', alpha=0.7, label='Korean Class', edgecolor='black')
    sp2.set_xlabel('Total Scores')
    sp2.set_ylabel('The number of students')
    sp2.set_title('Total Scores')
    sp2.legend()

    fig.savefig('class_score_plot.png', bbox_inches='tight')

    # Adjust to prevent overlap and plot
    plt.tight_layout()
    plt.show()
