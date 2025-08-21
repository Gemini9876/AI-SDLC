import React, { useState } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  StyleSheet, 
  Alert, 
  ActivityIndicator, 
  KeyboardAvoidingView, 
  Platform 
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { loginUser } from '../utils/api';
import { storeData } from '../utils/storage';
import { Colors } from '../styles/colors';

const LoginScreen = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigation = useNavigation();

  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('Login Error', 'Please enter both username and password.');
      return;
    }

    // Basic XSS/SQLi prevention: client-side validation for common patterns
    // Backend will handle robust sanitization and parameterized queries
    const sanitisedUsername = username.replace(/[<>&"'`]/g, ''); 
    const sanitisedPassword = password.replace(/[<>&"'`]/g, '');

    if (sanitisedUsername !== username || sanitisedPassword !== password) {
      Alert.alert('Security Alert', 'Invalid characters detected in input.');
      return;
    }

    setLoading(true);
    try {
      const response = await loginUser(username, password);
      await storeData('userToken', response.access_token);
      await storeData('userInfo', JSON.stringify(response.user));
      Alert.alert('Login Successful', 'Welcome to the Home Page!');
      navigation.replace('Home');
    } catch (error) {
      console.error('Login error:', error.response ? error.response.data : error.message);
      const errorMessage = error.response && error.response.data && error.response.data.detail
        ? error.response.data.detail
        : 'Login failed. Please check your credentials.';
      Alert.alert('Login Failed', errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView 
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : "height"}
    >
      <Text style={styles.title}>Welcome Back!</Text>
      
      <TextInput
        style={styles.input}
        placeholder="Username (e.g., frieda@example.com)"
        placeholderTextColor={Colors.placeholderText}
        value={username}
        onChangeText={setUsername}
        autoCapitalize="none"
        keyboardType="email-address"
        accessibilityLabel="Username input field"
        accessibilityHint="Enter your registered email address"
        returnKeyType="next"
        onSubmitEditing={() => this.passwordInput.focus()} // Logical tab order
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        placeholderTextColor={Colors.placeholderText}
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        accessibilityLabel="Password input field"
        accessibilityHint="Enter your password"
        ref={(input) => { this.passwordInput = input; }} // Logical tab order
        returnKeyType="done"
        onSubmitEditing={handleLogin}
      />
      
      <TouchableOpacity 
        style={styles.button}
        onPress={handleLogin}
        disabled={loading}
        accessibilityLabel="Login button"
        accessibilityHint="Tap to log in"
      >
        {loading ? (
          <ActivityIndicator color="#fff" accessibilityLabel="Loading indicator" />
        ) : (
          <Text style={styles.buttonText}>Log In</Text>
        )}
      </TouchableOpacity>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: Colors.background,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 30,
    color: Colors.primaryText,
    textAlign: 'center',
  },
  input: {
    width: '100%',
    padding: 15,
    borderWidth: 1,
    borderColor: Colors.borderColor,
    borderRadius: 8,
    marginBottom: 15,
    fontSize: 16,
    color: Colors.inputText,
    backgroundColor: Colors.inputBackground,
    // Ensure enough padding for easy tapping on mobile
  },
  button: {
    width: '100%',
    padding: 15,
    backgroundColor: Colors.primaryButtonBackground,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 10,
    // Ensure enough padding for easy tapping on mobile
  },
  buttonText: {
    color: Colors.primaryButtonText,
    fontSize: 18,
    fontWeight: 'bold',
    // WCAG: Ensure good contrast between button text and background
  },
});

export default LoginScreen;
