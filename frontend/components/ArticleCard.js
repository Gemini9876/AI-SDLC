import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, Dimensions } from 'react-native';
import { Colors } from '../styles/colors';

const { width } = Dimensions.get('window');

const ArticleCard = ({ article, onPress }) => {
  const isPaid = article.article_type === 'Paid';

  return (
    <TouchableOpacity 
      style={styles.card}
      onPress={onPress}
      accessibilityRole="button"
      accessibilityLabel={`View article: ${article.title}`}
      accessibilityHint={isPaid ? 'Premium content, requires paid subscription' : 'Free content'}
    >
      {article.image_url && (
        <Image 
          source={{ uri: `http://localhost:8000${article.image_url}` }} // Assuming backend serves images
          style={styles.image}
          accessibilityLabel={article.image_alt_text || `Image for article ${article.title}`}
          // Decorative images should have empty accessibilityLabel or be background images
          // For this example, assuming all images are informative.
        />
      )}
      
      <View style={styles.contentContainer}>
        <Text style={styles.title}>{article.title}</Text>
        <View style={[styles.badge, isPaid ? styles.badgePaid : styles.badgeFree]}>
          <Text style={styles.badgeText}>
            {isPaid ? 'Premium' : 'Free'}
          </Text>
        </View>
        <Text style={styles.description} numberOfLines={3}>
          {article.content.length > 100 ? article.content.substring(0, 97) + '...' : article.content}
        </Text>
        <Text style={styles.readMoreText}>Read More</Text>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: Colors.cardBackground,
    borderRadius: 10,
    marginVertical: 8,
    marginHorizontal: 10,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    flexDirection: width > 600 ? 'row' : 'column', // Responsive layout
    // Ensure enough tappable area on mobile
  },
  image: {
    width: width > 600 ? '30%' : '100%', // Responsive image width
    height: width > 600 ? 'auto' : 180, // Responsive image height
    aspectRatio: 16 / 9,
    resizeMode: 'cover',
  },
  contentContainer: {
    flex: 1,
    padding: 15,
    position: 'relative',
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: Colors.primaryText,
    marginBottom: 5,
    // WCAG: Ensure good contrast
  },
  badge: {
    position: 'absolute',
    top: 15,
    right: 15,
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: 5,
    justifyContent: 'center',
    alignItems: 'center',
    // Consistent positioning and styling for easy recognition
  },
  badgeFree: {
    backgroundColor: Colors.badgeFreeBackground,
  },
  badgePaid: {
    backgroundColor: Colors.badgePaidBackground,
  },
  badgeText: {
    color: Colors.badgeText,
    fontSize: 12,
    fontWeight: 'bold',
    // WCAG: Ensure good contrast
  },
  description: {
    fontSize: 14,
    color: Colors.secondaryText,
    marginTop: 10,
    marginBottom: 10,
    // WCAG: Ensure good contrast
  },
  readMoreText: {
    fontSize: 14,
    color: Colors.linkText,
    fontWeight: 'bold',
    alignSelf: 'flex-start',
    // WCAG: Ensure good contrast
  },
});

export default ArticleCard;
