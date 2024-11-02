from typing import Dict, Any, Set, List
import re

class TaskAnalyzer:
    def __init__(self):
        self.skill_keywords = {
            'self-evaluation': ['reflect', 'evaluate', 'assess'],
            'tool_usage': ['use', 'utilize', 'apply', 'tool'],
            'task_planning': ['plan', 'organize', 'structure'],
            'data_analysis': ['analyze', 'examine', 'investigate'],
            'problem_solving': ['solve', 'resolve', 'find solution'],
            'communication': ['communicate', 'express', 'convey'],
        }

    def identify_required_skills(self, task: Dict[str, Any]) -> Set[str]:
        skills = set()
        task_description = task.get('data', '').lower()
        
        for skill, keywords in self.skill_keywords.items():
            if any(keyword in task_description for keyword in keywords):
                skills.add(skill)
        
        if 'type' in task:
            if task['type'] == 'reflection':
                skills.add('self-evaluation')
            elif task['type'] == 'tool_usage':
                skills.add('tool_usage')
            elif task['type'] == 'planning':
                skills.add('task_planning')
        
        return skills

    def estimate_complexity(self, task: Dict[str, Any]) -> int:
        complexity = 1
        task_description = task.get('data', '')
        
        # Increase complexity based on word count
        word_count = len(task_description.split())
        complexity += min(word_count // 50, 5)  # Max 5 points for length
        
        # Increase complexity based on number of identified skills
        skills = self.identify_required_skills(task)
        complexity += len(skills)
        
        # Increase complexity for specific keywords
        complexity_keywords = ['complex', 'difficult', 'challenging', 'advanced']
        complexity += sum(keyword in task_description.lower() for keyword in complexity_keywords)
        
        return min(complexity, 10)  # Cap complexity at 10

    def identify_dependencies(self, task: Dict[str, Any]) -> List[str]:
        dependencies = task.get('dependencies', [])
        task_description = task.get('data', '')
        
        # Look for phrases like "after X" or "depends on Y"
        dependency_patterns = [
            r'after\s+(\w+)',
            r'depends\s+on\s+(\w+)',
            r'following\s+(\w+)',
        ]
        
        for pattern in dependency_patterns:
            dependencies.extend(re.findall(pattern, task_description, re.IGNORECASE))
        
        return list(set(dependencies))  # Remove duplicates

    def estimate_duration(self, task: Dict[str, Any]) -> float:
        base_duration = 0.5  # Base duration in hours
        complexity = self.estimate_complexity(task)
        
        # Adjust duration based on complexity
        duration = base_duration * complexity
        
        # Adjust duration based on specific time indicators in the task description
        task_description = task.get('data', '').lower()
        if 'quick' in task_description or 'brief' in task_description:
            duration *= 0.5
        elif 'thorough' in task_description or 'comprehensive' in task_description:
            duration *= 2
        
        return round(duration, 1)  # Round to one decimal place
