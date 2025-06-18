import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

export default function App() {
  const [history, setHistory] = useState([]);
  
  const handleDraw = (color) => {
    const newHistory = [...history, color].slice(-5); // nur die letzten 5
    setHistory(newHistory);
  };

  const handleUndo = () => {
    setHistory(history.slice(0, -1));
  };

  const redCount = history.filter(c => c === 'red').length;
  const blackCount = history.filter(c => c === 'black').length;
  const total = redCount + blackCount;

  const expectedProbability = {
    red: 0.5,
    black: 0.5,
  };

  const actualProbability = {
    red: total > 0 ? redCount / total : 0.5,
    black: total > 0 ? blackCount / total : 0.5,
  };

  const renderEmoji = (color) => {
    return color === 'red' ? '🟥' : '⬛';
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Schwarz oder Rot – Wahrscheinlichkeitsrechner</Text>

      <View style={styles.historyContainer}>
        <Text style={styles.historyLabel}>Letzte 5 Ziehungen:</Text>
        <Text style={styles.history}>
          {history.map((color, index) => (
            <Text key={index}>{renderEmoji(color)} </Text>
          ))}
        </Text>
      </View>

      <View style={styles.buttonRow}>
        <TouchableOpacity style={styles.redButton} onPress={() => handleDraw('red')}>
          <Text style={styles.buttonText}>Rot</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.blackButton} onPress={() => handleDraw('black')}>
          <Text style={styles.buttonText}>Schwarz</Text>
        </TouchableOpacity>
      </View>

      <TouchableOpacity style={styles.undoButton} onPress={handleUndo}>
        <Text style={styles.undoText}>⤺ Zurück</Text>
      </TouchableOpacity>

      <View style={styles.probabilityContainer}>
        <Text style={styles.probability}>Aktuelle Wahrscheinlichkeit:</Text>
        <Text style={styles.probability}>🟥 Rot: {(actualProbability.red * 100).toFixed(1)}%</Text>
        <Text style={styles.probability}>⬛ Schwarz: {(actualProbability.black * 100).toFixed(1)}%</Text>
        <Text style={styles.hintText}>(Erwartet: 50% / 50%)</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { fontSize: 20, fontWeight: 'bold', marginBottom: 20, textAlign: 'center' },
  historyContainer: { marginBottom: 20, alignItems: 'center' },
  historyLabel: { fontSize: 16 },
  history: { fontSize: 30, marginTop: 10 },
  buttonRow: { flexDirection: 'row', marginVertical: 20 },
  redButton: { backgroundColor: '#e74c3c', padding: 15, borderRadius: 10, marginHorizontal: 10 },
  blackButton: { backgroundColor: '#2c3e50', padding: 15, borderRadius: 10, marginHorizontal: 10 },
  buttonText: { color: 'white', fontWeight: 'bold' },
  undoButton: { marginBottom: 20 },
  undoText: { color: '#555', fontSize: 16 },
  probabilityContainer: { alignItems: 'center' },
  probability: { fontSize: 16, marginVertical: 2 },
  hintText: { fontSize: 12, color: '#999', marginTop: 10 },
});
