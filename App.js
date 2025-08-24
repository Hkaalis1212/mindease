import React, { useState, useCallback, useEffect, useContext } from 'react';
import { GiftedChat } from 'react-native-gifted-chat';
import { SafeAreaView, StyleSheet, Text, Alert } from 'react-native';
import { AuthProvider, AuthContext } from './AuthContext';
import ErrorBoundary from './ErrorBoundary';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState(null);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    setMessages([
      {
        _id: 1,
        text: 'Hello! How are you feeling today?',
        createdAt: new Date(),
        user: {
          _id: 2,
          name: 'AI Therapist',
        },
      },
    ]);
  }, []);

  const handleSend = useCallback(async (messages = []) => {
    setMessages(previousMessages =>
      GiftedChat.append(previousMessages, messages),
    );

    const message = messages[0];
    try {
      const response = await fetch('http://127.0.0.1:5000/journal', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ entry: message.text }),
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      console.log('Success:', data);
      setError(null);
    } catch (err) {
      console.error('Error:', err);
      setError('Unable to send message. Please try again later.');
      Alert.alert('Error', 'Unable to send message. Please try again later.');
    }
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      {error && <Text style={styles.errorText}>{error}</Text>}
      <GiftedChat
        messages={messages}
        onSend={handleSend}
        user={user}
      />
    </SafeAreaView>
  );
};

const App = () => (
  <AuthProvider>
    <ErrorBoundary>
      <Chat />
    </ErrorBoundary>
  </AuthProvider>
);

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  errorText: {
    color: 'red',
    textAlign: 'center',
    margin: 10,
  },
});

export default App;
