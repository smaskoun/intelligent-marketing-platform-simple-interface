import re
import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import hashlib

class EnhancedSEOContentService:
    """Enhanced service for generating diverse, non-repetitive SEO-optimized social media content"""
    
    def __init__(self):
        # Content memory to track recent generations
        self.content_memory = {
            'recent_templates': [],
            'recent_hooks': [],
            'recent_hashtags': [],
            'recent_topics': [],
            'generation_history': []
        }
        
        # Memory limits
        self.memory_limits = {
            'templates': 20,
            'hooks': 15,
            'hashtags': 30,
            'topics': 10,
            'history': 50
        }
        
        # Expanded template library (3x more templates)
        self.content_templates = {
            'property_showcase': {
                'hooks': [
                    "🏡 Just Listed in {location}!",
                    "✨ New Property Alert - {location}!",
                    "🔥 Hot Listing in {location}!",
                    "💎 Gem Found in {location}!",
                    "🌟 Featured Property - {location}!",
                    "🏠 Dream Home in {location}!",
                    "📍 Prime Location - {location}!",
                    "🎯 Perfect Match in {location}!",
                    "🔑 Your Next Home in {location}!",
                    "💫 Stunning Property in {location}!"
                ],
                'structures': [
                    "{hook}\n\n{property_highlights}\n\n{location_benefits}\n\n{call_to_action}",
                    "{hook}\n\n{unique_features}\n\n{lifestyle_appeal}\n\n{call_to_action}",
                    "{hook}\n\n{investment_angle}\n\n{market_context}\n\n{call_to_action}",
                    "{hook}\n\n{emotional_appeal}\n\n{practical_benefits}\n\n{call_to_action}",
                    "{hook}\n\n{neighborhood_focus}\n\n{property_value}\n\n{call_to_action}",
                    "{hook}\n\n{buyer_persona_focus}\n\n{property_match}\n\n{call_to_action}",
                    "{hook}\n\n{seasonal_appeal}\n\n{property_features}\n\n{call_to_action}",
                    "{hook}\n\n{comparison_advantage}\n\n{unique_selling_points}\n\n{call_to_action}"
                ]
            },
            'market_update': {
                'hooks': [
                    "📊 {location} Market Update:",
                    "📈 Latest Market Trends in {location}:",
                    "💹 {location} Real Estate Insights:",
                    "🏘️ Market Pulse - {location}:",
                    "📋 Your {location} Market Brief:",
                    "🎯 Market Focus: {location}",
                    "💡 Market Intelligence - {location}:",
                    "🔍 Market Analysis for {location}:",
                    "📌 {location} Market Spotlight:",
                    "⚡ Breaking Market News - {location}:"
                ],
                'structures': [
                    "{hook}\n\n{market_data}\n\n{trend_analysis}\n\n{buyer_seller_advice}\n\n{call_to_action}",
                    "{hook}\n\n{price_trends}\n\n{inventory_levels}\n\n{market_prediction}\n\n{call_to_action}",
                    "{hook}\n\n{comparative_analysis}\n\n{opportunity_highlight}\n\n{call_to_action}",
                    "{hook}\n\n{seasonal_trends}\n\n{timing_advice}\n\n{call_to_action}",
                    "{hook}\n\n{market_drivers}\n\n{impact_explanation}\n\n{call_to_action}",
                    "{hook}\n\n{buyer_market_conditions}\n\n{seller_market_conditions}\n\n{call_to_action}",
                    "{hook}\n\n{interest_rate_impact}\n\n{market_response}\n\n{call_to_action}",
                    "{hook}\n\n{local_economic_factors}\n\n{real_estate_correlation}\n\n{call_to_action}"
                ]
            },
            'educational': {
                'hooks': [
                    "💡 Home Buying Tip:",
                    "🎓 Real Estate 101:",
                    "📚 Did You Know?",
                    "🤔 Wondering About {topic}?",
                    "💭 Common Question:",
                    "🔍 Real Estate Myth Buster:",
                    "📖 Educational Moment:",
                    "🧠 Knowledge Drop:",
                    "💪 Empower Your Decision:",
                    "🎯 Pro Tip Alert:"
                ],
                'structures': [
                    "{hook}\n\n{educational_content}\n\n{practical_application}\n\n{call_to_action}",
                    "{hook}\n\n{myth_vs_reality}\n\n{correct_information}\n\n{call_to_action}",
                    "{hook}\n\n{step_by_step_guide}\n\n{key_takeaways}\n\n{call_to_action}",
                    "{hook}\n\n{common_mistake}\n\n{how_to_avoid}\n\n{call_to_action}",
                    "{hook}\n\n{industry_insight}\n\n{client_benefit}\n\n{call_to_action}",
                    "{hook}\n\n{process_explanation}\n\n{timeline_expectations}\n\n{call_to_action}",
                    "{hook}\n\n{cost_breakdown}\n\n{budgeting_advice}\n\n{call_to_action}",
                    "{hook}\n\n{legal_consideration}\n\n{protection_advice}\n\n{call_to_action}"
                ]
            },
            'community': {
                'hooks': [
                    "❤️ Love Our {location} Community!",
                    "🌟 Spotlight on {location}:",
                    "🏘️ Why {location} is Special:",
                    "📍 Local Favorite in {location}:",
                    "🎉 Celebrating {location}:",
                    "🌈 Community Pride - {location}:",
                    "🏆 {location} Excellence:",
                    "💖 Community Love - {location}:",
                    "🎪 Local Events in {location}:",
                    "🌻 {location} Lifestyle:"
                ],
                'structures': [
                    "{hook}\n\n{community_feature}\n\n{resident_benefits}\n\n{call_to_action}",
                    "{hook}\n\n{local_business_spotlight}\n\n{community_value}\n\n{call_to_action}",
                    "{hook}\n\n{community_event}\n\n{participation_benefits}\n\n{call_to_action}",
                    "{hook}\n\n{neighborhood_amenities}\n\n{lifestyle_appeal}\n\n{call_to_action}",
                    "{hook}\n\n{community_achievement}\n\n{pride_factor}\n\n{call_to_action}",
                    "{hook}\n\n{seasonal_community_activity}\n\n{engagement_opportunity}\n\n{call_to_action}",
                    "{hook}\n\n{local_culture}\n\n{community_identity}\n\n{call_to_action}",
                    "{hook}\n\n{community_support}\n\n{togetherness_message}\n\n{call_to_action}"
                ]
            }
        }
        
        # Expanded CTA library
        self.cta_templates = {
            'property_inquiry': [
                "DM me for exclusive details! 📩",
                "Ready for a private showing? Let's connect! 🔑",
                "Questions about this gem? I'm here to help! 💎",
                "Want the inside scoop? Message me! 📱",
                "Interested in learning more? Let's chat! 💬",
                "Ready to make this home yours? Reach out! 🏡",
                "Curious about the neighborhood? Let's explore! 🗺️",
                "Want to schedule a tour? I'm ready! 👥",
                "Need more photos? I've got them! 📸",
                "Ready to discuss your offer? Let's talk! 💼"
            ],
            'market_consultation': [
                "Want a personalized market analysis? Let's connect! 📊",
                "Curious about your home's current value? Let's discuss! 💰",
                "Ready to explore your options? I'm here to guide! 🧭",
                "Need market insights for your area? Reach out! 📈",
                "Planning your next move? Let's strategize! 🎯",
                "Want to understand the trends? Let's dive deep! 🔍",
                "Ready for a market consultation? I'm available! 📅",
                "Thinking of buying or selling? Let's plan! 📋",
                "Want expert market guidance? I'm here! 🎓",
                "Ready to make informed decisions? Let's connect! 🤝"
            ],
            'general_engagement': [
                "What's your take on this? Share below! 💭",
                "Have questions? Drop them in the comments! ⬇️",
                "Tag someone who needs to see this! 👥",
                "Save this for future reference! 🔖",
                "Share your experience in the comments! 💬",
                "What would you add to this list? Comment! ✍️",
                "Agree or disagree? Let me know! 🤷‍♀️",
                "Found this helpful? Share with friends! 🔄",
                "What's your biggest concern? Tell me! 😟",
                "Ready to take action? Let's go! 🚀"
            ]
        }
        
        # Synonym replacement system
        self.synonyms = {
            'beautiful': ['stunning', 'gorgeous', 'magnificent', 'breathtaking', 'spectacular'],
            'amazing': ['incredible', 'fantastic', 'wonderful', 'remarkable', 'outstanding'],
            'perfect': ['ideal', 'excellent', 'superb', 'flawless', 'pristine'],
            'great': ['excellent', 'fantastic', 'wonderful', 'terrific', 'superb'],
            'home': ['house', 'property', 'residence', 'dwelling', 'abode'],
            'buy': ['purchase', 'acquire', 'invest in', 'secure', 'obtain'],
            'sell': ['market', 'list', 'offer', 'present', 'showcase'],
            'location': ['area', 'neighborhood', 'district', 'community', 'region'],
            'opportunity': ['chance', 'possibility', 'prospect', 'opening', 'potential']
        }
        
        # Dynamic content variables
        self.dynamic_variables = {
            'seasonal_elements': {
                'spring': ['blooming', 'fresh', 'renewal', 'growth', 'vibrant'],
                'summer': ['sunny', 'bright', 'warm', 'active', 'outdoor'],
                'fall': ['cozy', 'comfortable', 'harvest', 'golden', 'crisp'],
                'winter': ['warm', 'inviting', 'shelter', 'comfort', 'peaceful']
            },
            'time_based': {
                'morning': ['start your day', 'morning coffee', 'sunrise', 'fresh start'],
                'afternoon': ['midday', 'lunch break', 'afternoon light', 'productive'],
                'evening': ['sunset', 'end of day', 'relaxing', 'peaceful evening']
            },
            'market_conditions': {
                'hot_market': ['competitive', 'fast-moving', 'high demand', 'quick sales'],
                'balanced_market': ['stable', 'steady', 'consistent', 'reliable'],
                'buyer_market': ['opportunities', 'choices', 'negotiation', 'value']
            }
        }
        
        # Location-specific data
        self.location_keywords = {
            'primary': [
                'Windsor', 'Essex County', 'Windsor-Essex', 'Windsor Ontario',
                'Essex', 'Kingsville', 'Leamington', 'Tecumseh', 'LaSalle',
                'Amherstburg', 'Belle River', 'Harrow'
            ],
            'neighborhoods': [
                'Downtown Windsor', 'Walkerville', 'Riverside', 'South Windsor',
                'East Windsor', 'West End', 'Forest Glade', 'Devonshire',
                'Sandwich', 'University District', 'Little Italy'
            ]
        }
    
    def generate_diverse_content(self, 
                               content_type: str,
                               platform: str = 'instagram',
                               location: str = None,
                               custom_data: Dict = None) -> Dict:
        """
        Generate diverse, non-repetitive content using memory system
        
        Args:
            content_type: Type of content to generate
            platform: Target platform
            location: Specific location
            custom_data: Additional customization data
        
        Returns:
            Dict containing diverse content and metadata
        """
        
        # Select location if not provided
        if not location:
            location = self._select_fresh_location()
        
        # Select template avoiding recent ones
        template_data = self._select_fresh_template(content_type)
        
        # Generate content with dynamic variables
        content = self._generate_dynamic_content(template_data, location, custom_data or {})
        
        # Apply synonym replacement
        content = self._apply_synonym_replacement(content)
        
        # Generate diverse hashtags
        hashtags = self._generate_diverse_hashtags(content_type, location, platform)
        
        # Update memory
        self._update_memory(template_data, content, hashtags)
        
        # Generate metadata
        metadata = self._generate_enhanced_metadata(content, location, content_type)
        
        return {
            'content': content,
            'hashtags': hashtags,
            'platform': platform,
            'location': location,
            'content_type': content_type,
            'metadata': metadata,
            'generation_id': self._generate_content_id(content),
            'timestamp': datetime.now().isoformat()
        }
    
    def _select_fresh_location(self) -> str:
        """Select a location that hasn't been used recently"""
        all_locations = self.location_keywords['primary'] + self.location_keywords['neighborhoods']
        recent_locations = [item.get('location') for item in self.content_memory['generation_history'][-5:]]
        
        available_locations = [loc for loc in all_locations if loc not in recent_locations]
        
        if not available_locations:
            available_locations = all_locations
        
        return random.choice(available_locations)
    
    def _select_fresh_template(self, content_type: str) -> Dict:
        """Select template components avoiding recent ones"""
        templates = self.content_templates[content_type]
        
        # Select hook avoiding recent ones
        recent_hooks = self.content_memory['recent_hooks']
        available_hooks = [hook for hook in templates['hooks'] if hook not in recent_hooks]
        if not available_hooks:
            available_hooks = templates['hooks']
        
        selected_hook = random.choice(available_hooks)
        
        # Select structure avoiding recent ones
        recent_templates = self.content_memory['recent_templates']
        available_structures = [struct for struct in templates['structures'] if struct not in recent_templates]
        if not available_structures:
            available_structures = templates['structures']
        
        selected_structure = random.choice(available_structures)
        
        return {
            'hook': selected_hook,
            'structure': selected_structure,
            'content_type': content_type
        }
    
    def _generate_dynamic_content(self, template_data: Dict, location: str, custom_data: Dict) -> str:
        """Generate content with dynamic variables"""
        
        # Get current season and time
        current_season = self._get_current_season()
        current_time = self._get_time_of_day()
        
        # Select dynamic elements
        seasonal_elements = random.sample(self.dynamic_variables['seasonal_elements'][current_season], 2)
        time_elements = random.sample(self.dynamic_variables['time_based'][current_time], 1)
        
        # Build content components
        hook = template_data['hook'].format(location=location, **custom_data)
        
        # Generate different content sections based on structure
        structure = template_data['structure']
        content_sections = {}
        
        if 'property_highlights' in structure:
            content_sections['property_highlights'] = f"This {seasonal_elements[0]} property features {seasonal_elements[1]} spaces perfect for {time_elements[0]}."
        
        if 'market_data' in structure:
            content_sections['market_data'] = f"Current market conditions in {location} show {seasonal_elements[0]} trends with {seasonal_elements[1]} opportunities."
        
        if 'educational_content' in structure:
            content_sections['educational_content'] = f"Understanding the {seasonal_elements[0]} market dynamics can help you make {seasonal_elements[1]} decisions."
        
        if 'community_feature' in structure:
            content_sections['community_feature'] = f"The {location} community offers {seasonal_elements[0]} amenities and {seasonal_elements[1]} lifestyle opportunities."
        
        # Add call to action
        cta_type = self._determine_cta_type(template_data['content_type'])
        recent_ctas = [item.get('cta') for item in self.content_memory['generation_history'][-3:]]
        available_ctas = [cta for cta in self.cta_templates[cta_type] if cta not in recent_ctas]
        if not available_ctas:
            available_ctas = self.cta_templates[cta_type]
        
        content_sections['call_to_action'] = random.choice(available_ctas)
        
        # Fill in any missing sections with generic content
        for section in ['location_benefits', 'unique_features', 'lifestyle_appeal', 'trend_analysis', 'practical_application']:
            if section in structure and section not in content_sections:
                content_sections[section] = f"Discover the {seasonal_elements[0]} advantages of {location}."
        
        # Format the final content
        try:
            final_content = structure.format(hook=hook, **content_sections)
        except KeyError as e:
            # Fallback if formatting fails
            final_content = f"{hook}\n\nExplore the {seasonal_elements[0]} opportunities in {location}.\n\n{content_sections['call_to_action']}"
        
        return final_content
    
    def _apply_synonym_replacement(self, content: str) -> str:
        """Apply synonym replacement to vary language"""
        words = content.split()
        
        for i, word in enumerate(words):
            word_lower = word.lower().strip('.,!?')
            if word_lower in self.synonyms:
                # 30% chance to replace with synonym
                if random.random() < 0.3:
                    synonym = random.choice(self.synonyms[word_lower])
                    # Preserve capitalization
                    if word[0].isupper():
                        synonym = synonym.capitalize()
                    words[i] = word.replace(word_lower, synonym)
        
        return ' '.join(words)
    
    def _generate_diverse_hashtags(self, content_type: str, location: str, platform: str) -> List[str]:
        """Generate diverse hashtags avoiding recent ones"""
        
        base_hashtags = {
            'property_showcase': ['#JustListed', '#NewListing', '#DreamHome', '#PropertyAlert', '#HomeForSale'],
            'market_update': ['#MarketUpdate', '#RealEstateNews', '#MarketTrends', '#PropertyMarket', '#MarketInsights'],
            'educational': ['#RealEstateTips', '#HomeBuyingTips', '#PropertyAdvice', '#RealEstateEducation', '#HomeSellingTips'],
            'community': ['#CommunityLove', '#LocalLife', '#Neighborhood', '#CommunitySpotlight', '#LocalBusiness']
        }
        
        # Location-based hashtags
        location_hashtags = [f"#{location.replace(' ', '').replace('-', '')}", f"#{location}RealEstate", f"#{location}Homes"]
        
        # General real estate hashtags
        general_hashtags = ['#RealEstate', '#Realtor', '#PropertyExpert', '#HomeExpert', '#RealEstateAgent']
        
        # Combine and select
        all_hashtags = base_hashtags[content_type] + location_hashtags + general_hashtags
        
        # Remove recently used hashtags
        recent_hashtags = [tag for sublist in self.content_memory['recent_hashtags'] for tag in sublist]
        available_hashtags = [tag for tag in all_hashtags if tag not in recent_hashtags[-20:]]
        
        if len(available_hashtags) < 8:
            available_hashtags = all_hashtags
        
        # Select appropriate number for platform
        if platform == 'instagram':
            selected_count = random.randint(8, 12)
        else:
            selected_count = random.randint(3, 5)
        
        selected_hashtags = random.sample(available_hashtags, min(selected_count, len(available_hashtags)))
        
        return selected_hashtags
    
    def _update_memory(self, template_data: Dict, content: str, hashtags: List[str]):
        """Update content memory to avoid repetition"""
        
        # Update recent templates
        self.content_memory['recent_templates'].append(template_data['structure'])
        if len(self.content_memory['recent_templates']) > self.memory_limits['templates']:
            self.content_memory['recent_templates'].pop(0)
        
        # Update recent hooks
        self.content_memory['recent_hooks'].append(template_data['hook'])
        if len(self.content_memory['recent_hooks']) > self.memory_limits['hooks']:
            self.content_memory['recent_hooks'].pop(0)
        
        # Update recent hashtags
        self.content_memory['recent_hashtags'].append(hashtags)
        if len(self.content_memory['recent_hashtags']) > self.memory_limits['hashtags']:
            self.content_memory['recent_hashtags'].pop(0)
        
        # Update generation history
        self.content_memory['generation_history'].append({
            'content_id': self._generate_content_id(content),
            'timestamp': datetime.now().isoformat(),
            'template': template_data['structure'],
            'hook': template_data['hook'],
            'hashtags': hashtags
        })
        
        if len(self.content_memory['generation_history']) > self.memory_limits['history']:
            self.content_memory['generation_history'].pop(0)
    
    def _get_current_season(self) -> str:
        """Get current season"""
        month = datetime.now().month
        if month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        elif month in [9, 10, 11]:
            return 'fall'
        else:
            return 'winter'
    
    def _get_time_of_day(self) -> str:
        """Get current time of day"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 17:
            return 'afternoon'
        else:
            return 'evening'
    
    def _determine_cta_type(self, content_type: str) -> str:
        """Determine appropriate CTA type"""
        if content_type == 'property_showcase':
            return 'property_inquiry'
        elif content_type == 'market_update':
            return 'market_consultation'
        else:
            return 'general_engagement'
    
    def _generate_content_id(self, content: str) -> str:
        """Generate unique ID for content"""
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def _generate_enhanced_metadata(self, content: str, location: str, content_type: str) -> Dict:
        """Generate enhanced metadata"""
        return {
            'word_count': len(content.split()),
            'character_count': len(content),
            'location_mentions': content.lower().count(location.lower()),
            'content_type': content_type,
            'uniqueness_score': self._calculate_uniqueness_score(content),
            'engagement_potential': self._estimate_engagement_potential(content, content_type)
        }
    
    def _calculate_uniqueness_score(self, content: str) -> float:
        """Calculate how unique this content is compared to recent generations"""
        recent_content = [item.get('content', '') for item in self.content_memory['generation_history'][-10:]]
        
        if not recent_content:
            return 1.0
        
        # Simple similarity check based on word overlap
        content_words = set(content.lower().split())
        similarity_scores = []
        
        for recent in recent_content:
            recent_words = set(recent.lower().split())
            if len(content_words) > 0 and len(recent_words) > 0:
                overlap = len(content_words.intersection(recent_words))
                similarity = overlap / len(content_words.union(recent_words))
                similarity_scores.append(similarity)
        
        if similarity_scores:
            avg_similarity = sum(similarity_scores) / len(similarity_scores)
            uniqueness = 1.0 - avg_similarity
        else:
            uniqueness = 1.0
        
        return max(0.0, min(1.0, uniqueness))
    
    def _estimate_engagement_potential(self, content: str, content_type: str) -> str:
        """Estimate engagement potential"""
        score = 0
        
        # Check for engagement elements
        if '?' in content:
            score += 10
        if any(word in content.lower() for word in ['you', 'your', 'we', 'us']):
            score += 15
        if any(emoji in content for emoji in ['🏡', '💡', '📊', '❤️', '🌟']):
            score += 10
        if len(content.split()) < 50:  # Optimal length
            score += 10
        
        if score >= 35:
            return 'high'
        elif score >= 20:
            return 'medium'
        else:
            return 'low'
    
    def get_content_analytics(self) -> Dict:
        """Get analytics on content generation patterns"""
        history = self.content_memory['generation_history']
        
        if not history:
            return {'message': 'No content generated yet'}
        
        # Analyze patterns
        template_usage = defaultdict(int)
        content_type_usage = defaultdict(int)
        uniqueness_scores = []
        
        for item in history:
            template_usage[item.get('template', 'unknown')] += 1
            uniqueness_scores.append(item.get('uniqueness_score', 0))
        
        return {
            'total_generated': len(history),
            'average_uniqueness': sum(uniqueness_scores) / len(uniqueness_scores) if uniqueness_scores else 0,
            'template_diversity': len(template_usage),
            'most_used_template': max(template_usage.items(), key=lambda x: x[1])[0] if template_usage else None,
            'memory_utilization': {
                'templates': f"{len(self.content_memory['recent_templates'])}/{self.memory_limits['templates']}",
                'hooks': f"{len(self.content_memory['recent_hooks'])}/{self.memory_limits['hooks']}",
                'hashtags': f"{len(self.content_memory['recent_hashtags'])}/{self.memory_limits['hashtags']}"
            }
        }

# Global instance
enhanced_seo_content_service = EnhancedSEOContentService()

