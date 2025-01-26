import json
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# Set the matplotlib backend to TkAgg
matplotlib.use('TkAgg')


# Load JSON data
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# Analyze performance by topics
def analyze_performance(quiz_data):
    topic_performance = {}
    for quiz in quiz_data:
        topic = quiz['quiz']['topic']

        # Safely get accuracy, default to 0 if not available
        accuracy = quiz.get('accuracy', '0%').strip('%')
        accuracy = float(accuracy) if accuracy else 0.0

        score = quiz.get('score', 0)
        correct_answers = quiz.get('correct_answers', 0)
        incorrect_answers = quiz.get('incorrect_answers', 0)

        if topic not in topic_performance:
            topic_performance[topic] = {
                'total_quizzes': 0,
                'total_accuracy': 0,
                'total_score': 0,
                'correct_answers': 0,
                'incorrect_answers': 0
            }
        topic_performance[topic]['total_quizzes'] += 1
        topic_performance[topic]['total_accuracy'] += accuracy
        topic_performance[topic]['total_score'] += score
        topic_performance[topic]['correct_answers'] += correct_answers
        topic_performance[topic]['incorrect_answers'] += incorrect_answers

    # Compute averages
    for topic in topic_performance:
        data = topic_performance[topic]
        data['average_accuracy'] = data['total_accuracy'] / data['total_quizzes']
        data['average_score'] = data['total_score'] / data['total_quizzes']

    return topic_performance


# Generate insights
def generate_insights(topic_performance):
    insights = []
    for topic, data in topic_performance.items():
        insights.append({
            'topic': topic,
            'weakness': data['incorrect_answers'],
            'strength': data['correct_answers'],
            'average_accuracy': data['average_accuracy'],
            'recommendation': f"Focus on improving accuracy in {topic}."
        })
    return insights


# Visualize trends
def visualize_trends(historical_data):
    scores = [quiz['score'] for quiz in historical_data]
    timestamps = [quiz['submitted_at'] for quiz in historical_data]

    plt.plot(timestamps, scores, marker='o')
    plt.title('Score Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Score')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as an image
    plt.savefig('score_trends.png')
    print("Plot saved as score_trends.png")


# Main Function
def main():
    # Load datasets
    current_quiz_data = load_json(r"C:\Users\LENOVO\Documents\assignments\Internshala\student dashboard\exam.json")
    current_quiz_submissions = load_json(
        r"C:\Users\LENOVO\Documents\assignments\Internshala\student dashboard\exam sub.json")
    historical_data = load_json(r"C:\Users\LENOVO\Documents\assignments\Internshala\student dashboard\sol.json")

    # Combine current and historical data
    combined_data = historical_data + [current_quiz_data] + [current_quiz_submissions]

    # Analyze performance
    topic_performance = analyze_performance(combined_data)

    # Generate insights
    insights = generate_insights(topic_performance)

    # Visualize trends
    visualize_trends(historical_data)

    # Print insights and recommendations
    print("\n--- Personalized Insights and Recommendations ---\n")
    for insight in insights:
        print(f"Topic: {insight['topic']}")
        print(f"  Weakness: {insight['weakness']}")
        print(f"  Strength: {insight['strength']}")
        print(f"  Average Accuracy: {insight['average_accuracy']:.2f}%")
        print(f"  Recommendation: {insight['recommendation']}\n")


# Execute main function
if __name__ == '__main__':
    main()
