import 'react-native-gesture-handler';
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import LoginScreen from './screens/LoginScreen';
import HomeScreen from './screens/HomeScreen';
import SubscriptionUpgradeScreen from './screens/SubscriptionUpgradeScreen';

const Stack = createStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Login">
        <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
        <Stack.Screen 
          name="Home" 
          component={HomeScreen} 
          options={{ 
            headerShown: true,
            title: 'Home',
            // Accessibility: Define header elements' focus order if needed
            // For mobile, typical usage is not full keyboard nav, but screen reader. 
            // Headers usually accessible automatically.
          }}
        />
        <Stack.Screen 
          name="SubscriptionUpgrade" 
          component={SubscriptionUpgradeScreen} 
          options={{ title: 'Upgrade Your Subscription' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default App;
