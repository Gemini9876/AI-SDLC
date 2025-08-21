import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { Colors } from '../styles/colors';

const SubscriptionUpgradeScreen = () => {
  return (
    <ScrollView contentContainerStyle={styles.container} accessibilityLabel="Subscription Upgrade Page">
      <Text style={styles.title}>Unlock Premium Content!</Text>
      <Text style={styles.description}>
        Upgrade your subscription to get unlimited access to all exclusive articles, videos, and more.
      </Text>

      <View style={styles.planCard} accessibilityRole="menuitem" accessibilityLabel="Basic Plan">
        <Text style={styles.planTitle}>Basic Plan</Text>
        <Text style={styles.planPrice}>$9.99 / month</Text>
        <Text style={styles.planFeature}>✓ Access to all Paid Articles</Text>
        <Text style={styles.planFeature}>✓ Ad-free experience</Text>
        <TouchableOpacity style={styles.button} accessibilityLabel="Choose Basic Plan">
          <Text style={styles.buttonText}>Choose Basic</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.planCard} accessibilityRole="menuitem" accessibilityLabel="Premium Plan">
        <Text style={styles.planTitle}>Premium Plan</Text>
        <Text style={styles.planPrice}>$19.99 / month</Text>
        <Text style={styles.planFeature}>✓ All Basic Plan features</Text>
        <Text style={styles.planFeature}>✓ Exclusive video content</Text>
        <Text style={styles.planFeature}>✓ Offline downloads</Text>
        <TouchableOpacity style={styles.button} accessibilityLabel="Choose Premium Plan">
          <Text style={styles.buttonText}>Choose Premium</Text>
        </TouchableOpacity>
      </View>

      <Text style={styles.footerText}>Questions? Contact support.</Text>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 20,
    backgroundColor: Colors.background,
    alignItems: 'center',
  },
  title: {
    fontSize: 26,
    fontWeight: 'bold',
    color: Colors.primaryText,
    marginBottom: 15,
    textAlign: 'center',
    // WCAG: Ensure good contrast
  },
  description: {
    fontSize: 16,
    color: Colors.secondaryText,
    textAlign: 'center',
    marginBottom: 30,
    // WCAG: Ensure good contrast
  },
  planCard: {
    backgroundColor: Colors.cardBackground,
    borderRadius: 10,
    padding: 20,
    marginVertical: 10,
    width: '100%',
    maxWidth: 400, // Max width for larger screens
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    // Responsive: Will naturally stack on small screens, center on large
  },
  planTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: Colors.primaryText,
    marginBottom: 10,
    // WCAG: Ensure good contrast
  },
  planPrice: {
    fontSize: 20,
    fontWeight: '600',
    color: Colors.accent,
    marginBottom: 20,
    // WCAG: Ensure good contrast
  },
  planFeature: {
    fontSize: 15,
    color: Colors.secondaryText,
    marginBottom: 8,
    textAlign: 'center',
    // WCAG: Ensure good contrast
  },
  button: {
    backgroundColor: Colors.primaryButtonBackground,
    paddingVertical: 12,
    paddingHorizontal: 25,
    borderRadius: 8,
    marginTop: 20,
    // Ensure enough padding for easy tapping on mobile
  },
  buttonText: {
    color: Colors.primaryButtonText,
    fontSize: 16,
    fontWeight: 'bold',
    // WCAG: Ensure good contrast
  },
  footerText: {
    marginTop: 30,
    fontSize: 14,
    color: Colors.tertiaryText,
    // WCAG: Ensure good contrast
  },
});

export default SubscriptionUpgradeScreen;
